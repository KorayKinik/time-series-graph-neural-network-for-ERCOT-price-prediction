# time-series-graph-neural-network-for-ERCOT-price-prediction
Forecasting locational electricity prices using spatio-temporal graph neural network 

Electricity is hard to store [1]. To match supply and demand real time and maintain a stable 60Hz voltage across the power grid, regulation mechanisms use optimization algorithms. For example, in Texas, ERCOT orchestrates over 1,250 power generation units by sending dispatch instructions every 5 minutes to maintain stable flow of power [2]. Yet, frequent congestions and outages cause volatility in local electricity prices [3]. This creates financial incentive for auxiliary generators and energy traders to predict day-ahead locational marginal prices (LMP). So far, most AI models focused on forecasting price in a single geo location [4]. However, the grid is a nodal network and each substation exchanges power with others regularly. 
In this work, I addressed this using a time series graph neural network approach to simulate the network. I trained a geometric temporal pytorch model [5] on 3 years’ worth of ERCOT data [6] in hourly resolution: historical prices and loads on all nodes, power flow between nodes, and transmission line capacities. The model successfully forecasted day-ahead LMPs at all 4,726 substations – except for intra-day spikes caused by local unplanned outages and transmission congestions.



![Slide1](https://github.com/user-attachments/assets/ee0bcd43-420e-4a39-87ab-704066f6f976)
![Slide2](https://github.com/user-attachments/assets/20fbaa62-08fb-42d1-ac01-028666d243f5)
![Slide3](https://github.com/user-attachments/assets/5d9746f6-8c5f-4a33-ade6-1fe255769d71)
![Slide4](https://github.com/user-attachments/assets/a1088147-7747-49d6-b174-f507ef69aab7)
![Slide5](https://github.com/user-attachments/assets/651bbb48-e0ca-44f3-a363-7eb7f147a76d)
![Slide6](https://github.com/user-attachments/assets/9c13e0a9-ae03-48ee-9805-7f3038cd0f90)
![Slide7](https://github.com/user-attachments/assets/21d17c05-e05c-4bb0-bf52-97395be8c937)
![Slide8](https://github.com/user-attachments/assets/63a2d490-99fe-43e9-a8fc-8b2c75ab26d2)
![Slide9](https://github.com/user-attachments/assets/394f5af4-4392-44d0-9b4d-a47f4f4e5489)
![Slide10](https://github.com/user-attachments/assets/fb5ad8c4-7e6e-4bc2-ab21-37094a216683)
![Slide11](https://github.com/user-attachments/assets/dbb94f62-0c8f-4c5e-a32d-06a4b28f072f)
![Slide12](https://github.com/user-attachments/assets/c29df3a6-f545-4db2-9eeb-bdb897f5df1d)
![Slide13](https://github.com/user-attachments/assets/b5ae9e67-92ed-47a2-8072-057cdd601e26)
![Slide14](https://github.com/user-attachments/assets/9bdf5ed2-0e68-4153-a3ad-8da1e18f32ad)
![Slide15](https://github.com/user-attachments/assets/6af39508-9e7d-4a24-bf06-04dfa7ba86bb)
![Slide16](https://github.com/user-attachments/assets/360c2dc1-96c1-4f35-a423-22f6efa30e15)
![Slide17](https://github.com/user-attachments/assets/0ab42fde-3c91-40ef-a176-f00a9c981eb1)
![Slide18](https://github.com/user-attachments/assets/9d439eda-5680-4e9f-adf3-ce112871d36f)
![Slide19](https://github.com/user-attachments/assets/b6f830a3-3a79-4b67-9f41-840c35fdac6a)
![Slide20](https://github.com/user-attachments/assets/29747f97-f31c-4065-bd2b-eb282356d2d3)
![Slide21](https://github.com/user-attachments/assets/1bd7cff8-2377-4f80-b916-20dd7e53d3f9)
![Slide22](https://github.com/user-attachments/assets/909a361d-17f2-4a06-b282-2634c17431b9)
![Slide23](https://github.com/user-attachments/assets/01042a4c-288d-49d1-b4d8-09589b33426b)
![Slide24](https://github.com/user-attachments/assets/006c57e5-e906-4b27-8d9a-a55e7b3647da)
![Slide25](https://github.com/user-attachments/assets/12d3ffa6-d70d-44c7-92ff-b187308e76e3)
![Slide26](https://github.com/user-attachments/assets/7e01d3e3-ca2a-418e-a580-669d0a0e594d)
![Slide27](https://github.com/user-attachments/assets/e63b3d12-808b-4e60-88e8-68f109054073)
![Slide28](https://github.com/user-attachments/assets/a820a7af-7f8f-4cbc-b483-648a1ced451f)
![Slide29](https://github.com/user-attachments/assets/aa7b30c4-8d04-4482-9350-9ac7670521cf)
