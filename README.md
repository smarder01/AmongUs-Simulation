# Among Us Simulation

This project simulates games of *Among Us* using real player stats from the Sidemen Plus channel on YouTube, where the Sidemen play *Among Us*. The goal is to analyze the probabilities of imposters or crewmates winning under different conditions. The data used in this simulation comes from an external GitHub repository, and this project builds upon that dataset.

## Features
- Simulates a standard *Among Us* game (2 imposters, rest crewmates).  
- Players perform actions based on real historical stats from the Sidemen Plus channel.  
- Tracks wins/losses for statistical analysis.  
- Randomized voting logic based on probability distributions.  

### Future Plans
- Add advanced roles (Jesters, Lovers, Engineers, etc.).
- Implement different *Among Us* maps and game settings.  
- Improve AI for more realistic player behavior.  
- Visualize game results with charts and graphs.  

## Data Source 

The player statistics used in this simulation come from [sidemen-AmongUsStats](https://github.com/Abe-neazer/sidemen-AmongUs-stats) by **Abeneazer Getachew Abeneazer**.  
All credit for data collection and compilation goes to them. This project builds upon their dataset to create a simulation of *Among Us* games.

If you are the original data creator and would like this attribution modified or removed, please let me know!  

### Sidemen Plus Channel
The gameplay data for this simulation is based on the *Sidemen Plus* YouTube channel, where the Sidemen play *Among Us* with various game modes and dynamics. The simulation mimics their gameplay style, with realistic behavior and interactions.

## Excel Sheets 📄  
The following sheets are used for this simulation:

1. **Player Stats**:  
   Contains information about each person who has played on the Sidemen Plus channel. The attributes include:  
   
   | **Attribute**             | **Description**                                                 | **Variable Type**      |
   |---------------------------|-----------------------------------------------------------------|------------------------|
   | Games Played              | Total number of games played by the player                     | Integer (count)        |
   | Wins                      | Number of games the player won                                  | Integer (count)        |
   | Losses                    | Number of games the player lost                                 | Integer (count)        |
   | Win %                     | Win percentage for the player                                   | Float (0-1)            |
   | Kills                     | Total kills made by the player                                  | Integer (count)        |
   | Deaths                    | Total times the player died                                     | Integer (count)        |
   | KDR (Kill-Death Ratio)    | Ratio of kills to deaths                                        | Float (ratio)          |
   | Kills as Imposter         | Total kills made as an imposter                                 | Integer (count)        |
   | Kills Per Imposter Game   | Average number of kills made per game as an imposter            | Float (count/game)     |
   | Imposter Games            | Total number of games the player played as an imposter          | Integer (count)        |
   | Imposter Wins             | Number of games the player won as an imposter                   | Integer (count)        |
   | Imposter Win %            | Win percentage as an imposter                                   | Float (0-1)            |
   | Crewmate Games            | Total number of games the player played as a crewmate           | Integer (count)        |
   | Crewmate Wins             | Number of games the player won as a crewmate                    | Integer (count)        |
   | Crewmate Win %            | Win percentage as a crewmate                                    | Float (0-1)            |
   | Neutral Games             | Number of games the player played as neutral                    | Integer (count)        |
   | Neutral Wins              | Number of games won as neutral                                  | Integer (count)        |
   | Neutral Win %             | Win percentage as neutral                                       | Float (0-1)            |
   | Lover Games               | Total number of games the player played as a lover              | Integer (count)        |
   | Lover Wins                | Number of games won as a lover                                  | Integer (count)        |
   | Lover Win %               | Win percentage as a lover                                       | Float (0-1)            |
   | Total Tasks               | Total number of tasks the player completed                      | Integer (count)        |
   | Tasks Completed           | Number of tasks completed by the player                         | Integer (count)        |
   | Task Completion %         | Percentage of tasks completed by the player                     | Float (0-1)            |
   | All Tasks Completed       | Number of games where all tasks were completed by the player    | Integer (count)        |
   | Voted Out                 | Number of times the player was voted out                        | Integer (count)        |
   | Emergency Meetings        | Number of emergency meetings the player called                  | Integer (count)        |
   | Bodies Reported           | Number of bodies the player reported                             | Integer (count)        |
   | Voted Out First           | Number of times the player was voted out first in a game        | Integer (count)        |
   | First Death of Game       | Number of times the player was the first to die in a game       | Integer (count)        |
   | Death in First Round      | Number of times the player died in the first round of a game   | Integer (count)        |
   | Disconnected              | Number of games the player disconnected from                   | Integer (count)        |
   | Rage Quit                 | Number of games the player rage quit                            | Integer (count)        |

2. **Imposter Combinations**:  
   Contains combinations of imposters and details about the games they were involved in, with the following attributes:  

   | **Attribute**         | **Description**                                              | **Variable Type**      |
   |-----------------------|--------------------------------------------------------------|------------------------|
   | Imposter Combination  | The combination of players acting as imposters               | String (Player List)   |
   | Number of Games       | Number of games this imposter combination played             | Integer (count)        |
   | Wins                  | Number of games this imposter combination won                | Integer (count)        |
   | Win %                 | Win percentage for this imposter combination                 | Float (0-1)            |

3. **Game Stats**:  
   Contains overall game statistics such as:  

   | **Attribute**                 | **Description**                                               | **Variable Type**      |
   |-------------------------------|---------------------------------------------------------------|------------------------|
   | Games Played                  | Total number of games played                                  | Integer (count)        |
   | Crewmate Wins by Tasks        | Number of crewmate wins by completing all tasks               | Integer (count)        |
   | Imposter Wins by Crises       | Number of imposter wins achieved by causing crises            | Integer (count)        |
   | Players Voted Out             | Number of players voted out                                   | Integer (count)        |
   | Emergency Meetings Called     | Number of emergency meetings called                           | Integer (count)        |
   | Bodies Reported               | Number of bodies reported during games                        | Integer (count)        |
   | Total Kills                   | Total number of kills across all games                        | Integer (count)        |
   | Total Tasks                   | Total number of tasks across all games                        | Integer (count)        |
   | Total Tasks Completed         | Total number of tasks completed across all games              | Integer (count)        |

## Installation

### Prerequisites
- Python 3.x  
- `pandas` (for handling Excel files)  

### Steps
1. Clone the repository:  
   ```sh
   git clone https://github.com/your-username/AmongUs-Simulation.git
