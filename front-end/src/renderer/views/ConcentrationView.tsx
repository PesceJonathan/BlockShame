import * as React from "react";
import ReactApexChart from "react-apexcharts";
import styled from "styled-components";
import Loader from "react-loader-spinner";
import RefreshIcon from "@material-ui/icons/Refresh";
import { startProgram } from "_utils/controller";
import {resolve} from "path";
var fs = require("fs");

const filename = "../VirtualWebcam/Data/ConcentrateArray.txt";
//const filename = "C:/Users/jonat/Desktop/BlockShame/VirtualWebcam/Data/ConcentrateArray.txt"
const fetchData = (setData: CallableFunction) => {
  fs.readFile(filename, "utf8", function (err: any, data: any) {
    if (err) {
      console.log("ERR" + err);
    }

    let array = data.split(",");
    array = array.map((point: any) => Math.round(parseFloat(point)));
    console.log("Fetched Concentration Data", data)
    setData(array);
  });
};

const Concentration = () => {
  const [data, setData] = React.useState([]);

  React.useEffect(() => {
    fetchData(setData);
  }, []);

  const chartData = getChartData(data);

  return (
    <Container>
      <Header>Concentration Tracker</Header>
      <Explanation>
        Keep track of the percentage of the time you were at your computer
        during the entire session!
      </Explanation>
      <RefreshIconStyled
        fontSize="large"
        onClick={() => {
          console.log(resolve(__dirname, "../", "../VirtualWebcam/ParseConcentrationData.py").toString())
          startProgram(
            resolve(__dirname, "../", "../VirtualWebcam/ParseConcentrationData.py").toString(),
            (code) => {
              if (code === 0) {
                console.log("Terminated python process")
                fetchData(setData);
              }
            }
          );
        }}
        style={{}}
      />
      {data.length === 0 ? (
        <LoaderContainer>
          <Loader type="Puff" color="#00BFFF" height={100} width={100} />
        </LoaderContainer>
      ) : (
        <ReactApexChart
          options={chartData.options}
          series={chartData.series}
          type="area"
          height={250}
          width={450}
        />
      )}
    </Container>
  );
};

export default Concentration;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  margin: 15px 15px 0px 15px;
  font-size: 20px;
`;
const RefreshIconStyled = styled(RefreshIcon)`
  cursor: pointer;
  align-self: flex-end;
`;

const Header = styled.div`
  margin-bottom: 20px;
  font-weight: bold;
`;

const Explanation = styled.div`
  margin-bottom: 50px;
  font-size: 16px;
`;

const LoaderContainer = styled.div`
  display: flex;
  width: 100%;
  justify-content: center;
  align-items: center;
`;

const getChartData = (data: number[]) => {
  return {
    series: [
      {
        name: "Concentration",
        data: data,
      },
    ],
    options: {
      chart: {
        width: 500,
        height: 350,
        type: "area",
        toolbar: {
          show: false,
        },
      },
      title: {
        text: "Percentage Of Time Concentrated",
        align: "left",
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        curve: "smooth",
      },
      xaxis: {
        categories: ["", "", "", "", ""],
      },
      yaxis: {
        min: 0,
        max: 100,
      },
    },
  };
};
