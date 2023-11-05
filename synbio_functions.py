from pacti.contracts import PolyhedralIoContract
def create_sensor_contracts(sensor_input="AHL", output="FP", K=0.0, yleak=0.0,
                            start=0.0, ymax_lin=0.0, ymax_sat=0.0, std=0.0, final_K=0.0):
    """
    Creates the contracts for a Marionette sensing subsystem
    params:
        * input (str): The inducer input to the sensor
        * output (str): The output of the genetic construct.
                        Inducer activates the production of this output
        * K (float): The value of the Hill activation parameter K
        * yleak (float): The minimum expression of output even
                         in absence of inducer
        * start (float): The value of inducer at which the induction starts
        * ymax_lin (float): The maximum expression of output by the inducer
                            before saturating (the end of linear regime)
        * ymax_sat (float): The absolute maximum value of the sensor after it saturates
        * std (float): The standard deviation for each value to create contracts
    """    
    yleak1 = yleak + std * yleak
    yleak2 = yleak - std * yleak
    ymax_lin1 = ymax_lin - std*ymax_lin
    ymax_lin2 = ymax_lin + std*ymax_lin
    ymax_sat1 = ymax_sat - std*ymax_sat
    ymax_sat2 = ymax_sat + std*ymax_sat
    
    off_slope1 = (0.1 * yleak1 - yleak1) / (0.08 * start - start)
    off_slope2 = (0.1 * yleak2 - yleak2) / (0.08 * start - start)
    off_intercept1 = yleak1 - off_slope1 * start
    off_intercept2 = yleak2 - off_slope2 * start
    lin_slope1 = (ymax_lin1 - yleak1) / (K - start)
    lin_slope2 = (ymax_lin2 - yleak2) / (K - start)
    lin_intercept1 = yleak1 - lin_slope1 * start
    lin_intercept2 = yleak2 - lin_slope2 * start
    
    sat_slope1 = (ymax_lin1 - ymax_sat1) / (K - final_K)
    sat_slope2 = (ymax_lin2 - ymax_sat2) / (K - final_K)
    sat_intercept1 = ymax_lin1 - sat_slope1 * K
    sat_intercept2 = ymax_lin2 - sat_slope2 * K
    contract_0 = PolyhedralIoContract.from_strings(
        input_vars=[sensor_input],
        output_vars=[output],
        assumptions=[f"{sensor_input} <= {start}",
                     f"-{sensor_input} <= -{0.08 * start}"
                    ],
        guarantees=[f"{output} - {off_slope1}{sensor_input} <= {off_intercept2}",
                    f"-{output} + {off_slope2}{sensor_input} <= {-1 * off_intercept1}"]
    )                
    contract_lin = PolyhedralIoContract.from_strings(
        input_vars=[sensor_input],
        output_vars=[output],
        assumptions=[
            f"{sensor_input} <= {K}",
            f"-{sensor_input} <= {-1 * start}"
        ],
        guarantees=[
            f"-{output} + {lin_slope1}{sensor_input} <= {-1 * lin_intercept1}",
            f"{output} - {lin_slope2}{sensor_input} <= {1 * lin_intercept2}"
        ]
    )
    contract_max = PolyhedralIoContract.from_strings(
        input_vars=[sensor_input],
        output_vars=[output],
        assumptions=[
            f"-{sensor_input} <= {-1 * K}",
            f"{sensor_input} <= {final_K}"
        ],
        guarantees=[
            f"{output} - {sat_slope2}{sensor_input} <= {sat_intercept2}",
            f"-{output} + {sat_slope1}{sensor_input} <= {-1 * sat_intercept1}"
        ]
    )
    return contract_0, contract_lin, contract_max

