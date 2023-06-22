#Streamlit
import streamlit as st
#Data manipulation
import pandas as pd
#NBA api
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import LeagueStandings
#Visualization
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px
#Requests
import requests
#Other
from io import BytesIO

st.set_page_config(
     page_title="NBA Recap",
     page_icon=":basketball:",
     layout="centered",
     initial_sidebar_state="expanded")

header = st.container()
awards = st.container()
leaders = st.container()
standings = st.container()
shotchart = st.container()
pergame = st.container()

#CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

#Firstly, let's create a function that reads data from basketballreference.com and makes the necessary adjustments
def read_data(year):
    #Reading per-game table from basketballrefence
    url = f"https://www.basketball-reference.com//leagues/NBA_{year}_per_game.html"
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest"}
    r = requests.get(url, headers=header)
    dfs = pd.read_html(r.text)
    df = dfs[0]

    #Manipulating dataframe
    df.drop(['Rk'], axis=1, inplace = True)

    def single_row(df): #this is a function to eliminate duplicate players
        if df.shape[0] == 1:
            return df
        else:
            row = df[df["Tm"]=="TOT"]
            row["Tm"] = df.iloc[-1,:]["Tm"]
            return row

    df = df.groupby(['Player']).apply(single_row)
    df.index = df.index.droplevel()

    df.fillna(0, inplace = True)

    #Cleaning player column
    df['Player'] = df['Player'].str.replace("*", "", regex=False)
    df['Player'] = df['Player'].str.replace("ć", "c").str.replace("č", "c").str.replace(" Jr", " Jr.").str.replace("A.J. Hammons", "AJ Hammons").str.replace("A.J. Price", "AJ Price")

    for column in df.columns: #this for loop converts the columns to floats
        if column not in ['Player', 'Pos', 'Tm']:
            df[column]=df[column].astype(float)

    return df

with header:
    st.title("NBA Recap :basketball:")
    st.write("A simple web-app to recap NBA seasons: awards winners, league leaders, standings, shot-charts and complete per game stats!")

with st.sidebar:
    st.write("### Input your information here!")

    all_teams = ['ATL','BOS','BRK','CHI','CHO','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM',
                 'MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS']
    
    all_teams_dict = {'ATL' : 'Atlanta Hawks', 'BOS' : 'Boston Celtics', 'BRK' : 'Brooklyn Nets',
                      'CHO' : 'Charlotte Hornets', 'CHI' : 'Chicago Bulls', 'CLE' : 'Cleveland Cavaliers', 
                      'DAL' : 'Dallas Mavericks', 'DEN' : 'Denver Nuggets', 'DET' : 'Detroit Pistons',
                      'GSW' : 'Golden State Warriors', 'HOU' : 'Houston Rockets', 'IND' : 'Indiana Pacers',
                      'LAC' : 'Los Angeles Clippers', 'LAL' : 'Los Angeles Lakers', 'MEM' : 'Memphis Grizzlies',
                      'MIA' : 'Miami Heat', 'MIL' : 'Milwaukee Bucks', 'MIN' : 'Minnesota Timberwolves',
                      'NOP' : 'New Orleans Pelicans', 'NYK' : 'New York Knicks', 'OKC' : 'Oklahoma City Thunder',
                      'ORL' : 'Orlando Magic', 'PHI' : 'Philadelphia 76ers', 'PHO' : 'Phoenix Suns',
                      'POR' : 'Portland Trail Blazers', 'SAC' : 'Sacramento Kings', 'SAS' : 'San Antonio Spurs',
                      'TOR' : 'Toronto Raptors', 'UTA' : 'Utah Jazz', 'WAS' : 'Washington Wizards'}

    all_positions = ['PG', 'SG', 'SF', 'PF', 'C']

    #Input year
    st.write("#### :point_right: Season input")
    year = st.selectbox("Select the NBA season you want to recap", list(reversed(range(1980, 2024))))
    year_adjusted = str(year-1)+'-'+str(year)[2:]

    #Season leaders
    st.write("#### :point_right: Season leaders inputs")
    stats = st.multiselect("What stat are you interested in?", ['PTS', 'AST', 'TRB', 'BLK', 'STL', 'TOV', 'FG%', 'FT%', '3P%', 'eFG%'], 'PTS')

    #Shot chart
    st.write("#### :point_right: Shot chart inputs")
    players_list = list(read_data(year)['Player'])
    if "Stephen Curry" in players_list:
        default_player = "Stephen Curry"
    elif "LeBron James" in players_list:
        default_player = "LeBron James"
    elif "Kobe Bryant" in players_list:
        default_player = "Kobe Bryant"
    else:
        default_player = "Shaquille O'Neal"
    shotchart_player = st.selectbox("Type player name for the shot chart", players_list, index = players_list.index(default_player))
    
    #Per game stats
    st.write("#### :point_right: Per game stats inputs")
    teams = st.multiselect('Select the teams for the per game stats', all_teams, all_teams)
    positions = st.multiselect('Select the positions for the per game stats', all_positions, all_positions)

with awards:
    st.write("## Awards")
    st.write(f"Check out the award winners of the {year_adjusted} season!")

    #Reading awards table
    awards = pd.read_excel('resources/nba-awards.xlsx', sheet_name='Awards')

    def get_awards_winners(year):
        return {'champion':awards[awards['year']==year].iloc[0]['champion'],
                'finals_mvp':awards[awards['year']==year].iloc[0]['finals_mvp'],
                'mvp':awards[awards['year']==year].iloc[0]['mvp'],
                'dpoy':awards[awards['year']==year].iloc[0]['dpoy'],
                'roty':awards[awards['year']==year].iloc[0]['roty'],
                'mip':awards[awards['year']==year].iloc[0]['mip'],
                'sixth_man':awards[awards['year']==year].iloc[0]['6th_man'],
                'coty':awards[awards['year']==year].iloc[0]['coty']}

    awards_winners = get_awards_winners(year)

    st.write(f"- **Champions**: {awards_winners['champion']} \n - **Finals Most Valuable Player**: {awards_winners['finals_mvp']} \n - **Most Valuable Player**: {awards_winners['mvp']} \n - **Defensive Player of the Year**: {awards_winners['dpoy']} \n - **Rookie of the Year**: {awards_winners['roty']} \n - **Most Improved Player**: {awards_winners['mip']} \n - **Sixth Man of the Year**: {awards_winners['sixth_man']} \n - **Coach of the Year**: {awards_winners['coty']}")

with leaders:
    st.markdown("""---""")
    st.write("## Regular season leaders")
    leaders_df = read_data(year)
    
    #Getting top 5 for each category

    def get_top5(stat, df): #this function gets top5 players depending on the stat selected
        #https://www.nba.com/stats/help/statminimums/
        if stat == 'FG%' or 'eFG%':
            #Minimum of 300 field goals made
            top5 = df[(df['G']*df['FG']>=300)][['Player',stat]].sort_values(stat, ascending=False, ignore_index=True).head(5)
        if stat == 'FT%':
            #Minium of 125 free throws made
            top5 = df[(df['G']*df['FT']>=125)][['Player',stat]].sort_values(stat, ascending=False, ignore_index=True).head(5)
        if stat == '3P%':
            #Minium of 82 3 pointers made
            top5 = df[(df['G']*df['3P']>=82)][['Player',stat]].sort_values(stat, ascending=False, ignore_index=True).head(5)
        else:
            top5 = df[['Player',stat]].sort_values(stat, ascending=False, ignore_index=True).head(5)
        return top5

    if len(stats)>0:
        #Description
        st.write(f"Here you can go through the top 5 leaders for a variety of stats of the {year_adjusted} season. PTS is automatically selected, but you can select the stats you want to check out in the **Season leaders inputs** sidebar section.")
        st.write(f"**_Tip_**: hover over the bars to check out the exact averages.")

        #Plotting leaders
        for stat in stats:
            top5 = get_top5(stat, leaders_df)
            fig = px.bar(top5, x=top5.columns[0], y=top5.columns[1], title=f"{year_adjusted} {stat} leaders")
            fig.update_traces(marker_color='#1D4289')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(':warning: Select stats in the sidebar.')

with standings:
    st.markdown("""---""")
    st.write("## Regular season standings")

    standings = LeagueStandings(season=year_adjusted).get_data_frames()[0]
    standings = standings.sort_values(['Conference','PlayoffRank'])[['PlayoffRank', 'Conference', 'TeamName', 'WinPCT', 'Record', 'HOME', 'ROAD', 'PreAS', 'PostAS']]
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(standings)

with shotchart:
    st.markdown("""---""")
    st.write("## Shot charts")

    #Description
    st.write("This is where you can check out regular season shot charts for your favourite players. Just type in the player name in the **Shot chat inputs** sidebar section and we are good to go.")
    st.write("**_Disclaimer_**: unfortunately, shot chart data only goes back to the 1996-97 season, when the NBA first started tracking play-by-play data.")

    if year <= 1996:
        st.warning(':warning: Shot chart data is only available from 1996-97 onwards.')
    
    else:
        if len(shotchart_player)>0:
            sc_players = players.get_players()

            #Function to get a player id based on its full nmame
            def get_player_id(fullName):
                for player in sc_players:
                    if player['full_name'] == fullName:
                        return player['id']
                return -1

            #Function to draw basketball court
            def create_court(ax, color):
                # Short corner 3PT lines
                ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
                ax.plot([220, 220], [0, 140], linewidth=2, color=color)
            
                # 3PT Arc
                ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))
                
                # Lane and Key
                ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
                ax.plot([80, 80], [0, 190], linewidth=2, color=color)
                ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
                ax.plot([60, 60], [0, 190], linewidth=2, color=color)
                ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
                ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))
                
                # Rim
                ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))

                # Backboard
                ax.plot([-30, 30], [40, 40], linewidth=2, color=color)
                
                # Remove ticks
                ax.set_xticks([])
                ax.set_yticks([])
                
                # Set axis limits
                ax.set_xlim(-250, 250)
                ax.set_ylim(0, 470)
                
                # General plot parameters
                mpl.rcParams['font.family'] = 'DejaVu Sans'
                mpl.rcParams['font.size'] = 10
                mpl.rcParams['axes.linewidth'] = 2

            #Get player shotlog from ShotChartDetail endpoint
            player_shotlog = shotchartdetail.ShotChartDetail(team_id = 0, 
                                                    player_id = get_player_id(shotchart_player),
                                                    context_measure_simple = 'FGA',
                                                    season_nullable = year_adjusted,
                                                    season_type_all_star = ['Regular Season', 'Playoffs'])

            #Extract dataframes
            player_df = player_shotlog.get_data_frames()[0]
            player_fgm = player_df.loc[player_df['SHOT_MADE_FLAG']==1]
            player_missed = player_df.loc[player_df['SHOT_MADE_FLAG']==0]

            # Draw basketball court
            fig = plt.figure(figsize=(2*4, 2*3.76))
            ax = fig.add_axes([0, 0, 1, 1])

            # Add player shots
            ax.scatter(player_missed['LOC_X'], player_missed['LOC_Y'] + 60, alpha=0.4, color='Red', label='Missed')
            ax.scatter(player_fgm['LOC_X'], player_fgm['LOC_Y'] + 60, alpha=0.4, color='Green',label='Made')

            # Annotate player name and season
            ax.text(0, 1.02, f'{shotchart_player}\n{year_adjusted} Regular Season', transform=ax.transAxes, ha='left', va='baseline')

            # Save graph and show plot
            ax = create_court(ax, 'black')
            plt.legend(loc="best")
            st.pyplot(fig)

with pergame:
    st.markdown("""---""")
    st.write("## Complete per-game stats")

    #Reading data
    pergame = read_data(year)

    #For loop to convert the columns to strings so we don't have an excess of decimals
    for column in pergame.columns:
        if column not in ['Player', 'Pos', 'Tm']:
            pergame[column]=pergame[column].astype(str)

    if len(teams)>0 and len(positions)>0:
        #Description
        st.write("This is a full per game table based on your selections in the **Per game stats inputs** sidebar section. All teams and positions are automatically selected, but you can change it according to your preferences.")
        st.write("**_Tip_**: you can download your data in MS Excel format on the download button bellow.")
        #Filtering teams and positions
        pergame = pergame[(pergame['Tm'].isin(teams)) & (pergame['Pos'].isin(positions))].reset_index(drop=True)

        #Showing dataframe
        st.dataframe(pergame)
        st.write(f'Data dimension: {pergame.shape[0]} rows and {pergame.shape[1]} columns')
        
        #Function to export to excel
        def to_excel(df):
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1')
            writer.close()
            processed_data = output.getvalue()
            return processed_data
        
        excel = to_excel(pergame)

        st.download_button(
            label="Download per game stats",
            data=excel,
            file_name='nba-recap-per-game.xlsx',
            mime='text/csv',
         )

    else:
        st.warning(':warning: Select teams and positions in the sidebar.')