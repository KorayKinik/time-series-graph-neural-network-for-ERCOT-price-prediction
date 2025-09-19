# time-series-graph-neural-network-for-ERCOT-price-prediction
Forecasting locational electricity prices using spatio-temporal graph neural network 

Electricity is hard to store [1]. To match supply and demand real time and maintain a stable 60Hz voltage across the power grid, regulation mechanisms use optimization algorithms. For example, in Texas, ERCOT orchestrates over 1,250 power generation units by sending dispatch instructions every 5 minutes to maintain stable flow of power [2]. Yet, frequent congestions and outages cause volatility in local electricity prices [3]. This creates financial incentive for auxiliary generators and energy traders to predict day-ahead locational marginal prices (LMP). So far, most AI models focused on forecasting price in a single geo location [4]. However, the grid is a nodal network and each substation exchanges power with others regularly. 
In this work, I addressed this using a time series graph neural network approach to simulate the network. I trained a geometric temporal pytorch model [5] on 3 years’ worth of ERCOT data [6] in hourly resolution: historical prices and loads on all nodes, power flow between nodes, and transmission line capacities. The model successfully forecasted day-ahead LMPs at all 4,726 substations – except for intra-day spikes caused by local unplanned outages and transmission congestions.


![Slide1](https://github.com/user-attachments/assets/8b7bcce8-a14e-41c4-9da4-a34eb7fd9803)
![Slide2](https://github.com/user-attachments/assets/84f5b608-d768-4bc2-9137-b6f5fd1b3078)
![Slide3](https://github.com/user-attachments/assets/2b4e66fa-c447-45b2-bda6-75f6ac00f14c)
![Slide4](https://github.com/user-attachments/assets/212119f1-ab87-48c0-80ac-e5f7fc3bcfb1)
![Slide5](https://github.com/user-attachments/assets/36707c9a-689c-4a18-b94d-1ae8698e76e3)
![Slide6](https://github.com/user-attachments/assets/cf4f4eeb-8dba-4b9e-a5f9-c6b623177ed1)
![Slide7](https://github.com/user-attachments/assets/a3ff36c7-5a29-4ae3-a0f6-5df9812aa33f)
![Slide8](https://github.com/user-attachments/assets/fa015cc2-b1b7-4d7b-aa32-0b77ed27d56d)
![Slide9](https://github.com/user-attachments/assets/765db22c-870d-425b-a94b-169a666df58d)
![Slide10](https://github.com/user-attachments/assets/177d9541-5400-458c-b5e6-0b66a9d7eca2)
![Slide11](https://github.com/user-attachments/assets/92d100ba-ba07-44d5-a759-2537d33721ba)
![Slide12](https://github.com/user-attachments/assets/a97501fa-ab04-46c3-8ceb-85a6e31daf6a)
![Slide13](https://github.com/user-attachments/assets/5c72f936-fafd-4111-8f05-fac8d7a7ad75)
![Slide14](https://github.com/user-attachments/assets/72551466-f30e-4627-be35-e2674a9a93b8)
![Slide15](https://github.com/user-attachments/assets/1cd70cea-3b2c-4694-819b-a920718239dc)
![Slide16](https://github.com/user-attachments/assets/d92135b7-6369-43af-9c1e-87f2bcc0b036)
![Slide17](https://github.com/user-attachments/assets/aed5cc67-2827-4f0c-90fd-13d20db99b46)
![Slide18](https://github.com/user-attachments/assets/e6991090-df6a-4813-9db5-38c8e36549ff)
![Slide19](https://github.com/user-attachments/assets/135c2210-0ef3-489a-8f9d-8d47ca1eac54)
![Slide20](https://github.com/user-attachments/assets/2293a84f-daa8-4ed9-91c7-41124c03b353)
![Slide21](https://github.com/user-attachments/assets/521ad4e2-e2b6-417f-9d36-f84401874a9e)
![Slide22](https://github.com/user-attachments/assets/fb21f59d-ba5b-4924-9425-177fb83272b4)
![Slide23](https://github.com/user-attachments/assets/e123e88b-ce15-4a70-ac1f-e37c12b7597d)
![Slide24](https://github.com/user-attachments/assets/b4643dac-c422-464d-9389-eadb2cf749fa)
![Slide25](https://github.com/user-attachments/assets/c8dcbc35-68e0-49d9-97e9-4235eb2374f7)
![Slide26](https://github.com/user-attachments/assets/717ef645-cc99-4267-9931-67382fea13d2)
![Slide27](https://github.com/user-attachments/assets/eed20164-92d7-49b6-b42f-152013e4c2f0)
![Slide28](https://github.com/user-attachments/assets/b6ac4512-943d-43cb-b4f7-eff62ee3feed)
![Slide29](https://github.com/user-attachments/assets/a541da02-e50a-4d4d-b083-8d583b0d2fb2)
