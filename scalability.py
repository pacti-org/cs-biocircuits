# Design and Computational Scalability with Pacti

import itertools
import time
import pandas as pd
import numpy as np
from pacti.terms.polyhedra import PolyhedralContract
from pacti.terms.polyhedra.polyhedra import Var
from pacti.utils import write_contracts_to_file
from utils.synbio_utils import create_sensor_contracts2

# Read the data from the paper using the CSV file "marionette_data.csv"
df = pd.read_csv("data/marionette_data.csv", delimiter=",", engine="python")

# Add the new "std" column with random values between 0.1 and 0.3
df["std"] = np.random.uniform(0.7, 0.8, len(df))

# Write the updated DataFrame to a new CSV file
df.to_csv("data/marionette_data_with_std.csv", index=False)

# Create all sensor contracts:
sensor_names = [str(i) for i in df["Inducer"]]
sensor_library = {}
sensor_library_params = {}
for sensor in sensor_names:
    sensor_params = {}
    yleak_s = df.loc[df["Inducer"] == sensor]["ymin (RPUx10-3)"].values[0]
    yleak_s = yleak_s * 1e-3
    s_start = df.loc[df["Inducer"] == sensor]["start"].values[0]
    s_K = df.loc[df["Inducer"] == sensor]["K (µM)"].values[0]
    ymax_s = df.loc[df["Inducer"] == sensor]["ymax Linear"].values[0]
    std = df.loc[df["Inducer"] == sensor]["std"].values[0]
    sensor_params = {"leak": yleak_s, "start": s_start, "K": s_K, "ymax": ymax_s, "std": std}
    s_output = "dCas9"
    contract_s_0, contract_s_lin, contract_s_max = create_sensor_contracts2(
        sensor_input=sensor, output="xRFP", start=s_start, K=s_K, ymax_lin=ymax_s, yleak=yleak_s, std=std
    )
    sensor_library[sensor] = [contract_s_0, contract_s_lin, contract_s_max]
    sensor_library_params[sensor] = sensor_params

outputs = ["x1", "x2", "x3", "x4"]

processor_1 = PolyhedralContract.from_string(
    input_vars=["x1", "x2"],
    output_vars=["y1"],
    assumptions=[
        f"-x1 <= {-1 * 0.02}",
        f"-x2 <= {-1 * 0.01}",
    ],
    guarantees=[
        "-y1 <= -2.05",
    ],
)
processor_2 = PolyhedralContract.from_string(
    input_vars=["x3", "x4"],
    output_vars=["y2"],
    assumptions=[
        f"-x3 <= {-1 * 0.07}",
        f"-x4 <= {-1 * 0.08}",
    ],
    guarantees=[
        "-y2 <= -1.05",
    ],
)
processor_3 = PolyhedralContract.from_string(
    input_vars=["y1", "y2"],
    output_vars=["y"],
    assumptions=[
        f"-y1 <= {-1 * 0.4}",
        f"-y2 <= {-1 * 0.5}",
    ],
    guarantees=[
        "-y <= -2.05",
    ],
)

from typing import Optional, Tuple
from pacti_instrumentation.pacti_counters import PactiInstrumentationData

save_contracts: bool = False
save_errors: bool = False


def explore_combination(count, combo) -> Tuple[PactiInstrumentationData, Optional[PolyhedralContract]]:
    # For this iteration of chosen sensors to use
    # compute the contracts and store them in a list
    sys_contract = None
    errors_log = []
    for sensor, output_i in zip(combo, outputs):
        # For "sensor" input and "output_i" output, we get the contracts:
        contract_s_0, contract_s_lin, contract_s_max = create_sensor_contracts2(
            sensor_input=sensor,
            output=output_i,
            start=sensor_library_params[sensor]["start"],
            K=sensor_library_params[sensor]["K"],
            ymax_lin=sensor_library_params[sensor]["ymax"],
            yleak=sensor_library_params[sensor]["leak"],
            std=sensor_library_params[sensor]["std"],
        )
        if output_i == "x1":
            # Store the contract for the sensor with output "x1"
            sensor1 = contract_s_max
        elif output_i == "x2":
            # Compose the sensor with output "x2" with the stored sensor "sensor1"
            try:
                composed_sensor12 = contract_s_max.compose(sensor1)
            except Exception as e:
                composed_sensor12 = None
                errors_log.append(e)
            # Now, compose 1+2 with processor_1
            if composed_sensor12 is not None:
                try:
                    composed_subsys1 = composed_sensor12.compose(processor_1)
                except Exception as e:
                    composed_subsys1 = None
                    errors_log.append(e)
            else:
                composed_subsys1 = None
        if output_i == "x3":
            # Store the contract for the sensor with output "x3"
            sensor3 = contract_s_max
        elif output_i == "x4":
            # Compose the sensor with output "x2" with the stored sensor "sensor1"
            try:
                composed_sensor34 = contract_s_max.compose(sensor3)
            except Exception as e:
                composed_sensor34 = None
                errors_log.append(e)
            # Now, compose 3+4 with processor_2, if composed_sensor34 was successful
            # if composed_sensor34 is not None:
            try:
                composed_subsys2 = composed_sensor34.compose(processor_2)
            except Exception as e:
                composed_subsys2 = None
                errors_log.append(e)
        else:
            composed_subsys2 = None
        # else:
        # If composition of sensor 1 and 2 is None,
        # then no point computing the composition of 3 and 4 with processor2.
        # composed_subsys2 = None
    if composed_subsys1 is not None and composed_subsys2 is not None:
        try:
            composed_subsys = composed_subsys1.compose(composed_subsys2)
            sys_contract = composed_subsys.compose(processor_3)
        except Exception as e:
            composed_subsys = None
            sys_contract = None
            errors_log.append(e)

    if sys_contract is not None:
        # Verify whether the final composed system has correct inputs and outputs
        try:
            for sensor in combo:
                assert Var(sensor) in sys_contract.inputvars
            assert Var("y") in sys_contract.outputvars
        except AssertionError as e:
            errors_log.append(e)

    if save_errors:
        with open("data/design_error_log_" + str(count) + ".txt", "w") as f:
            for error in errors_log:
                f.write(str(error))

    if save_contracts:
        write_contracts_to_file(
            [sys_contract], ["contract_" + str(count)], "data/successful_design_" + str(count) + ".json"
        )

    return PactiInstrumentationData().update_counts(), sys_contract

