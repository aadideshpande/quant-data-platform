FASTAPI link: https://fastapi.tiangolo.com/tutorial/first-steps/

### **Instructions:**

1) Install required packages from requirements.txt
2) Run main.py
3) open http://localhost:8000/docs on the web browser
4) Run case_study.py

**main.py:** 
Contains list of all endpoints

**models.py:**
Create dummy data

**security.py:**
Implement the authentication mechanism for users to access proprietary data



**How to test authorization?**

1) Try using the /proprietary-info endpoint
2) Click on the "Authorize" on the top-right and enter username: **johndoe** and password: **secret**
3) Try using the same endpoint again



### **Endpoints:** 

| API                                  | Body Example                                                         | API Description                                            |
|--------------------------------------|----------------------------------------------------------------------|------------------------------------------------------------|
| POST /api/advanced_sentence_search/  | {"sentence": "analyze the prices of energy stocks during inflation"} | get a list of all relevant datasets                        |
| GET /api/metadata                    | -                                                                    | get a list of all available datasets                       |                                   | 
| GET /api/news/sentiment_score_filter | -                                                                    | get the news articles for a stock based on sentiment value |
| GET /api/get-stock-data              | -                                                                    | get yahoo finance stock data                               |
| GET /api/datasets/{tag_name}         | -                                                                    | get the relevant datasets for a given tag                  |
| GET /api/advanced_search             | -                                                                    |                                                            |

