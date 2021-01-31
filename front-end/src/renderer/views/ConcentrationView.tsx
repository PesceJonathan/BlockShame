import * as React from 'react';
import ReactApexChart from 'react-apexcharts';
import styled from "styled-components";

const Concentration = () => {
    return (
        <Container>
            <Header>Concentration Tracker</Header>
            <Explanation>Keep track of the percentage of the time you were at your computer during the entire session!</Explanation>
            <ReactApexChart options={chartData.options} series={chartData.series} type="area" height={250} width={450}/>
        </Container>
    )
  }
   
export default Concentration;


const Container = styled.div`
    display: flex;
    flex-direction: column;
    margin: 15px 15px 0px 15px;
    font-size: 20px;
`

const Header = styled.div`
    margin-bottom: 20px;
    font-weight: bold;
`

const Explanation = styled.div`
    margin-bottom: 50px;
    font-size: 16px;
`

const chartData = {
          
    series: [{
      name: 'Concentration',
      data: [31, 40, 28, 95, 34]
    }],
    options: {
      chart: {
        width: 500,
        height: 350,
        type: 'area',
        toolbar: {
            show: false
        }
      },
      title: {
        text: 'Percentage Of Time Concentrated',
        align: 'left'
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: 'smooth'
      },
      xaxis: {
        categories: ['', '', '', '', ''],
      }
    },
}