"""Test the PIconnect package."""

import asyncio

import PIconnect as PI
import PIconnect._time as PItime
from PIconnect import PIData, _async


async def get_point_value(tag: str):
    """Get the value of a PI point asynchronously."""
    with PI.PIServer() as server:
        point = server.search("P140_11_053_FQIS_01_TotCumulatiefAct")[0]
        starttime = "2024-01-01"
        endtime = "2024-01-02"
        time_range = PItime.to_af_time_range(starttime, endtime)
        boundarytype = PI.AF.Data.AFBoundaryType.Inside
        filterexpression = ""
        token = _async.CancellationToken().token
        values = _async.task_to_future(
            point.pi_point.RecordedValuesAsync(
                time_range,
                boundarytype,
                filterexpression,
                False,
                0,
                token,
            )
        )

        # print("Point: ", point)
        # print(dir(point.pi_point))
        print(values)

        value1 = PIData.PISeries.from_afvalues(
            await values,
            tag=point.name,
            units_of_measurement=point.units_of_measurement,
        )
        print(value1)

        value2 = point.recorded_values_async(starttime, endtime)
        print(value2)
        print(await value2)
        # print(values.Result)
    return values


async def main():
    """Run the program."""
    print("Hello ...")
    await asyncio.sleep(0.1)
    print("... World!")


async def runall():
    """Run all the functions."""
    await asyncio.gather(main(), get_point_value("P140_11_053_FQIS_01_TotCumulatiefAct"))


if __name__ == "__main__":
    asyncio.run(runall())
