# 🍄🥾 Spores & Outdoors 🍀🥾

🍄🥾✨ *Is today better for mushrooms or hiking?*   🍄🥾✨
Spores & Outdoors is a playful weather-based app that helps nature and hiking lovers decide whether to go **mushroom foraging** or **hiking** or **both** or **neither**! Powered by real-time weather conditions ✨.

## 🌐 Live Demo
**[Try the app now!](https://spores-outdoors-iuuvvacjpqlqmg6ejunewm.streamlit.app)** 🚀
*Experience the magic of weather-based outdoor recommendations in real-time!*

---

## 🚀 Features
- 🌤️ Fetch live weather data from OpenWeatherMap API  
- 🍄 Calculate a **Mushroom Score** (is it damp and cool enough?)  
- 🥾 Calculate a **Hiking Score** (is it clear and comfortable?)  
- 🎨 Friendly **Streamlit UI** for instant answers  
- 📊 Expandable with **historical analysis and data science models**  

---

## 🧩 Tech Stack
- **Python** - Core programming language
- **Streamlit** - Interactive web app framework
- **OpenWeatherMap API** - Real-time weather data
- **Pandas** - Data manipulation and analysis
- **Streamlit Community Cloud** - Deployment platform

---

## 📂 Project Structure
```
├── app/
│   ├── advisor.py          # Core recommendation logic
│   ├── api_fetcher.py      # Weather API integration
│   ├── db.py              # Database operations
│   ├── streamlit_app.py   # Main Streamlit interface
│   ├── background2.jpg    # UI background image
│   └── bg_cool_clear.jpg  # Alternative background
├── data/                  # Data storage directory
├── notebooks/            # Jupyter notebooks for analysis
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- OpenWeatherMap API key ([Get one here](https://openweathermap.org/api))

### Quick Start
1. **Clone the repository**
   ```bash
   git clone git@github.com:ferdaousbouzaiene/Spores-Outdoors.git
   cd spores-outdoors
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

4. **Run the app locally**
   ```bash
   streamlit run app/streamlit_app.py
   ```

5. **Open your browser** to `http://localhost:8501`

---

## 🌐 Deployment

### Streamlit Community Cloud
This app is deployed on **Streamlit Community Cloud** for easy access and sharing.

#### Deployment Steps
1. **Push code to GitHub** with proper secrets management
2. **Connect to Streamlit Cloud** at [share.streamlit.io](https://share.streamlit.io)
3. **Configure secrets** in the Streamlit Cloud dashboard:
   ```toml
   # .streamlit/secrets.toml
   OPENWEATHER_API_KEY = "your_api_key_here"
   ```
4. **Deploy** and share your live app URL!

#### Environment Configuration
- **Python version**: 3.9+
- **Dependencies**: Managed via `requirements.txt`
- **Secrets**: Stored securely in Streamlit Cloud
- **Auto-deployment**: Enabled on main branch updates

---

## 🎯 How It Works

### Scoring Algorithm
The app evaluates weather conditions using two custom scoring systems:

**🍄 Mushroom Score Factors:**
- **Humidity** (higher is better)
- **Temperature** (cooler is better) 
- **Recent precipitation** (moisture encourages growth)
- **Cloud cover** (overcast conditions preferred)

**🥾 Hiking Score Factors:**
- **Temperature** (comfortable range preferred)
- **Precipitation** (dry conditions favored)
- **Wind speed** (moderate winds acceptable)
- **Visibility** (clear skies preferred)

### Decision Matrix
| Mushroom Score | Hiking Score | Recommendation |
|---------------|--------------|----------------|
| High | High | **Perfect day for both!** 🍄🥾 |
| High | Low | **Great for mushroom foraging** 🍄 |
| Low | High | **Ideal hiking weather** 🥾 |
| Low | Low | **Maybe stay indoors** 🏠 |

---

## 🔧 Configuration

### Weather Parameters
Customize scoring weights in `app/advisor.py`:
```python
MUSHROOM_WEIGHTS = {
    'humidity': 0.4,
    'temperature': 0.3,
    'precipitation': 0.2,
    'cloud_cover': 0.1
}

HIKING_WEIGHTS = {
    'temperature': 0.35,
    'precipitation': 0.30,
    'wind_speed': 0.20,
    'visibility': 0.15
}
```

---

## 📊 Future Enhancements

### Planned Features
- [ ] **Historical data analysis** - Track seasonal patterns
- [ ] **Location-based recommendations** - Multiple city support
- [ ] **Machine learning models** - Improve scoring accuracy
- [ ] **User preferences** - Personalized recommendations
- [ ] **Social features** - Share adventures with friends
- [ ] **Mushroom species database** - Species-specific foraging advice
- [ ] **Trail difficulty integration** - Match weather to trail conditions
- [ ] **Mobile optimization** - Enhanced mobile experience
- [ ] **Notification system** - Weather alerts for perfect conditions

### Data Science Opportunities
- **Time series forecasting** for optimal foraging/hiking windows
- **Clustering analysis** of weather patterns
- **Feature engineering** for improved scoring algorithms
- **A/B testing** different recommendation strategies
- **User behavior analytics** from deployed app usage

---

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** and add tests
4. **Test locally** before submitting
5. **Commit your changes** (`git commit -m 'Add amazing feature'`)
6. **Push to the branch** (`git push origin feature/amazing-feature`)
7. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Include unit tests for new features
- Test deployment compatibility
- Update documentation as needed

---

## 📈 Usage Analytics

Want to track how your deployed app is being used? Consider adding:
- **Streamlit Analytics** for user engagement metrics
- **Custom logging** for recommendation patterns
- **Feedback collection** for user satisfaction

---

## 🙏 Acknowledgments

- **OpenWeatherMap** for providing reliable weather data
- **Streamlit** team for the amazing framework and free hosting
- **Streamlit Community** for deployment support
- **Mushroom foraging community** for inspiration
- **Hiking enthusiasts** who love outdoor adventures

---

**Happy foraging and hiking!** 🍄🥾✨

---

*Built with ❤️ for nature and mushroom lovers everywhere | Deployed with 🚀 Streamlit Community Cloud*
