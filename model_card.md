# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
 **Jamitup 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

The recommender to suggest built on user profile: assumes consistency in the user profile 
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The model uses each song's genre, mood, energy level, and acousticness to match against a user's favorite genre, preferred mood, target energy, and whether they like acoustic music, calculating a score by awarding points for exact matches and measuring how close the energy levels are, while I added acoustic preference and refined the weights from the starter logic to better handle conflicting user tastes.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The dataset contains 18 songs in the catalog, representing a variety of genres including pop, lofi, rock, ambient, jazz, synthwave, indie pop, country, classical, hip hop, reggae, metal, folk, electronic, and blues, with moods ranging from happy and chill to intense, relaxed, moody, focused, nostalgic, dreamy, confident, soulful, energetic, romantic, playful, and melancholic; I did not add or remove any data from the original starter dataset, but parts of musical taste are missing such as regional or cultural music styles, and while attributes like danceability, tempo, and valence are present in the data, they are not used in the current scoring logic.  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works well for users with consistent preferences, such as those who strongly prefer a specific genre like pop or lofi, correctly capturing patterns where matching genre and mood lead to higher scores, and the recommendations often matched my intuition for straightforward profiles where energy levels aligned closely.  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The system does not consider features like danceability, tempo, or valence that could refine recommendations, genres like world music or underrepresented moods like euphoric are missing, it overfits to genre preference due to high weighting, and unintentionally favors users with mainstream genre tastes while marginalizing those with niche or conflicting preferences.  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested various user profiles including adversarial ones like high-energy sad pop fans and low-energy electronic users, looking for how well the system handled conflicting preferences and maintained reasonable scores. Genre dominated over mood and energy mismatches, and I ran simple tests in the main.py script to compare recommendations across different profiles.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

I would incorporate additional features like valence for better mood matching and tempo for energy refinement, improve explanations by highlighting trade-offs in conflicting preferences, increase diversity by adding serendipity bonuses for non-genre matches, and handle complex tastes by allowing multi-genre or mood preferences.  I would also seek a bigger dataset to improve training nad test whether we can change the weighting system's performance by gaining feedback from customer satisfaction

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps

I learned that recommender systems can create filter bubbles by over-weighting certain features, discovered that even simple scoring can reveal biases like genre dominance, and this experience made me more aware of how music apps might limit discovery by prioritizing exact matches over nuanced preferences.  
