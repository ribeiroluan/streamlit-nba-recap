# streamlit-nba-recap

### Description

This web app was created as a part of exploring `Streamlit` as a method to deploy data projects. It is directed to people who, like me, love NBA basketball and want to recap the main events from seasons going back to 1980 - award winners, season leaders, shot charts for individual players, per game stats.

Check it out!

<p align = "center">
    <img src="nba-recap-demo.gif" width = 900>
</p>

### Data sources

The Streamlit web app pulls data from two main sources based on the selections on the app widgets.
- [Basketball Reference](https://www.basketball-reference.com/): per game stats are scrapped directly from Basketball Reference. Meanwhile, the awards winners data is a  static table pulled from Basketball Reference, given that it does not need constant updates.
- [NBA API](https://github.com/swar/nba_api): the shot chart graph sends requests to the NBA API to pull the data of made and missed shots.

### How to deploy the web app

I tried to deploy the web app using `Heroku`, but had some challenges. The web app does not fully work due to the fact that the NBA API blocks requests coming from cloud providers, which are used by Heroku. You can check the app [here](https://nba-seasons-recap.herokuapp.com/). Therefore, I am leaving a sugestion on how to run the web app locally.

```
git clone https://github.com/ribeiroluan/streamlit-nba-recap

# change to project repository
cd streamlit-nba-recap

# install requirements
pip install -r requirements.txt

# use streamlit to run the app
streamlit run app.py
```

### References

- Chanin Nantasenamat (Data Professor) - [Build 12 Data Science Apps with Python and Streamlit](https://www.youtube.com/watch?v=JwSS70SZdyM): that's where I got the idea from.
- Lloyd Hung - [A Beginner’s Guide: Using the NBA API to obtain data for Shot Charts](https://lloydhung.medium.com/a-beginners-guide-using-the-nba-api-to-obtain-data-for-shot-charts-part-1-799c679f99e1): helped me build the shot chart graph.
- kfoofw [repository](https://github.com/kfoofw/nba-shot-chart-streamlit#readme): helped me write this README.
