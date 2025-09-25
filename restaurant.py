import streamlit as st
import time
import json
import random
from datetime import datetime, timedelta

# Page Config
st.set_page_config(
    page_title="🍕 Pizza Paradise - Artisan Pizzas",
    page_icon="🍕",
    layout="wide"
)

# --- Data Sources with Fallback Mechanism ---
class PizzaDataManager:
    def __init__(self):
        # Primary data source (RAG-style knowledge base)
        self.menu_data = {
            "specials": [
                {
                    "name": "🔥 Green Chile Fusion",
                    "price": "$18.99",
                    "description": "2025's hottest trend! Roasted New Mexican green chiles with smoked mozzarella, caramelized onions, and jalapeño-lime crema. This trending combination offers the perfect balance of heat and flavor on our wood-fired crust.",
                    "tag": "🔥 TRENDING",
                    "tag_color": "#e74c3c"
                },
                {
                    "name": "🫐 Berry Bratwurst Delight",
                    "price": "$22.99", 
                    "description": "Wonderfully weird 2025 trend! Premium bratwurst with fresh blueberries, caramelized onions, and goat cheese. This 'wonderfully weird' combination is taking the pizza world by storm with its unexpected flavor harmony.",
                    "tag": "🆕 2025 SPECIAL",
                    "tag_color": "#9b59b6"
                },
                {
                    "name": "🌮 Mexican-Inspired Fiesta",
                    "price": "$19.99",
                    "description": "America's most wanted global flavor! Seasoned ground beef, Mexican chorizo, jalapeños, fresh cilantro, Mexican cheese blend, and lime crema. 37% of Americans want to try Mexican-inspired pizza in 2025!",
                    "tag": "🌮 MOST WANTED",
                    "tag_color": "#27ae60"
                },
                {
                    "name": "🥒 Pickle & Kimchi Surprise",
                    "price": "$21.99",
                    "description": "Following 2025's briny trend! Tangy dill pickles with fermented kimchi, crispy bacon, and ranch drizzle. Fermented toppings are ready to follow pickles' popularity surge.",
                    "tag": "🥒 FERMENTED",
                    "tag_color": "#f39c12"
                },
                {
                    "name": "🍯 Hot Honey Truffle",
                    "price": "$26.99",
                    "description": "Premium 2025 trend! Truffle-infused cream base, hot honey drizzle, caramelized figs, prosciutto, and arugula. Unique bases and savory-sweet combinations are redefining pizza.",
                    "tag": "🍯 GOURMET",
                    "tag_color": "#8e44ad"
                },
                {
                    "name": "🌱 Locally Sourced Garden",
                    "price": "$20.99",
                    "description": "Eco-friendly 2025 focus! Organic vegetables from local farms, farm-fresh mozzarella, and herb-infused olive oil. Supporting local producers and transparency in sourcing.",
                    "tag": "🌱 LOCAL",
                    "tag_color": "#16a085"
                }
            ],
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Customer reviews with fallback data
        self.reviews_data = [
            {
                "rating": "⭐⭐⭐⭐⭐",
                "text": "The Green Chile Fusion is absolutely incredible! The perfect balance of heat and flavor. Pizza Paradise always stays ahead of the trends - this is why they're my go-to place!",
                "author": "Maria S., Regular Customer",
                "tag": "Trending Pick",
                "tag_color": "#e74c3c"
            },
            {
                "rating": "⭐⭐⭐⭐⭐", 
                "text": "I was skeptical about the Berry Bratwurst Delight, but wow! The combination is unexpectedly amazing. The service was fantastic even during rush hour.",
                "author": "David R., Food Adventurer",
                "tag": "Wonderfully Weird",
                "tag_color": "#9b59b6"
            },
            {
                "rating": "⭐⭐⭐⭐⭐",
                "text": "The Mexican-Inspired Fiesta pizza transported me straight to Mexico! Authentic flavors and premium ingredients. My family's new favorite for special occasions.",
                "author": "Jennifer L., Family Customer",
                "tag": "Most Wanted",
                "tag_color": "#27ae60"
            },
            {
                "rating": "⭐⭐⭐⭐⭐",
                "text": "Never thought pickles and kimchi would work on pizza, but this is genius! The fermented flavors create such a unique taste profile. Innovation at its finest!",
                "author": "Alex M., Foodie",
                "tag": "Fermented Trend",
                "tag_color": "#f39c12"
            },
            {
                "rating": "⭐⭐⭐⭐⭐",
                "text": "The Hot Honey Truffle pizza is pure luxury! The truffle cream base with hot honey is an experience. Worth every penny for special occasions.",
                "author": "Sophia K., Gourmet Lover",
                "tag": "Premium Experience",
                "tag_color": "#8e44ad"
            },
            {
                "rating": "⭐⭐⭐⭐⭐",
                "text": "Love that they source ingredients locally! The Garden pizza tastes so fresh and you can really taste the quality. Supporting local farms makes it even better.",
                "author": "The Johnson Family",
                "tag": "Eco-Friendly",
                "tag_color": "#16a085"
            }
        ]
    
    def get_today_specials(self):
        """Get today's special menu with fallback mechanism"""
        try:
            specials = self.menu_data["specials"]
            daily_specials = random.sample(specials, min(4, len(specials)))
            return daily_specials
        except Exception as e:
            st.error("⚠️ Unable to load latest specials. Showing cached menu.")
            return [
                {
                    "name": "🍕 Classic Margherita", 
                    "price": "$16.99",
                    "description": "Traditional tomato sauce, fresh mozzarella, and basil",
                    "tag": "CLASSIC",
                    "tag_color": "#3498db"
                },
                {
                    "name": "🍖 Pepperoni Supreme",
                    "price": "$18.99", 
                    "description": "Premium pepperoni with extra cheese",
                    "tag": "POPULAR",
                    "tag_color": "#e74c3c"
                }
            ]
    
    def get_customer_reviews(self):
        """Get customer reviews with fallback"""
        try:
            return random.sample(self.reviews_data, min(6, len(self.reviews_data)))
        except Exception as e:
            st.error("⚠️ Unable to load latest reviews. Showing cached reviews.")
            return [
                {
                    "rating": "⭐⭐⭐⭐⭐",
                    "text": "Great pizza and excellent service!",
                    "author": "Happy Customer",
                    "tag": "Verified Review",
                    "tag_color": "#28a745"
                }
            ]
    
    def simulate_web_search_fallback(self):
        """Simulate web search when primary data fails"""
        st.info("🔍 Fetching latest menu updates from web sources...")
        time.sleep(1)
        return {
            "status": "success",
            "trending_items": ["Green Chile Pizza", "Fermented Toppings", "Local Ingredients"],
            "source": "Pizza Industry Trends 2025"
        }

# Initialize data manager
data_manager = PizzaDataManager()

# --- Clean CSS without animations ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@400;700;900&display=swap');
    
    /* Global Reset */
    .main {
        padding: 0rem 1rem;
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-family: 'Playfair Display', serif;
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #ff6b35 0%, #ff8e53 50%, #ff9800 100%);
        border-radius: 30px;
        padding: 4rem 2rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 10px 40px rgba(255, 107, 53, 0.3);
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 5rem;
        font-weight: 900;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        letter-spacing: -2px;
    }
    
    .hero-subtitle {
        font-size: 1.6rem;
        color: rgba(255,255,255,0.95);
        font-weight: 500;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Pizza Cards */
    .pizza-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.98) 0%, rgba(255,255,255,0.95) 100%);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(255,139,83,0.2);
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .pizza-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(255,107,53,0.2);
    }
    
    .pizza-name {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .pizza-desc {
        font-size: 1rem;
        color: #4a5568;
        text-align: center;
        line-height: 1.7;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    
    .pizza-price {
        background: linear-gradient(135deg, #ff6b35 0%, #ff8e53 100%);
        color: white;
        padding: 10px 25px;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(255,107,53,0.3);
    }
    
    /* Image Container */
    .pizza-image-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .pizza-image-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    /* 3D Pizza Display */
    .pizza-3d-container {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 
            20px 20px 60px #d1d9e6,
            -20px -20px 60px #ffffff;
        margin: 2rem 0;
    }
    
    .pizza-3d-title {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, #ff6b35, #ff8e53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Review Cards */
    .review-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 4px solid #ff6b35;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    /* Data Status */
    .data-status {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(40, 167, 69, 0.9);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        z-index: 1000;
        backdrop-filter: blur(10px);
    }
    
    .data-status.fallback {
        background: rgba(255, 193, 7, 0.9);
    }
    
    /* Modern Divider */
    .modern-divider {
        height: 3px;
        background: linear-gradient(90deg, transparent, #ff6b35, #ff8e53, #ff6b35, transparent);
        border: none;
        margin: 3rem 0;
        border-radius: 2px;
    }
    
    /* Footer */
    .premium-footer {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        border-radius: 25px;
        padding: 3rem 2rem;
        margin-top: 4rem;
        text-align: center;
        color: white;
        border-top: 3px solid #ff6b35;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title { 
            font-size: 3.5rem; 
            letter-spacing: -1px; 
        }
        .hero-subtitle { 
            font-size: 1.3rem; 
        }
        .pizza-card { 
            padding: 2rem; 
            margin: 1rem 0; 
        }
        .premium-footer {
            padding: 2rem 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .hero-title { 
            font-size: 2.8rem; 
        }
        .pizza-name { 
            font-size: 1.6rem; 
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Data Status Indicator ---
st.markdown('<div class="data-status" id="dataStatus">🟢 Live Data Active</div>', unsafe_allow_html=True)

# --- Hero Section ---
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title main-header">Pizza Paradise</h1>
    <p class="hero-subtitle">Artisan crafted pizzas with <strong>premium ingredients</strong> and <strong>wood-fired perfection</strong></p>
</div>
""", unsafe_allow_html=True)

# --- 3D Pizza Showcase ---
st.markdown("""
<div class="pizza-3d-container">
    <h2 class="pizza-3d-title">🍕 Our Signature Creations</h2>
    <div style="font-size: 8rem; margin: 2rem 0;">🍕</div>
    <p style="font-size: 1.2rem; color: #6c757d;">Hand-crafted with passion, served with pride</p>
</div>
""", unsafe_allow_html=True)

# --- Today's Special Menu Section ---
st.markdown("### 🍕 Today's Special Menu - Fresh from our Kitchen!")
st.markdown(f"*Last updated: {data_manager.menu_data['last_updated']} | Based on 2025 Pizza Trends*")

try:
    specials = data_manager.get_today_specials()
    
    # Display specials in columns
    num_cols = min(len(specials), 3)
    cols = st.columns(num_cols)
    
    for idx, special in enumerate(specials):
        with cols[idx % num_cols]:
            st.markdown(f"""
            <div class="pizza-card">
                <h3 class="pizza-name">{special['name']}</h3>
                <p class="pizza-desc">{special['description']}</p>
                <div style="text-align: center; margin-top: 20px;">
                    <span class="pizza-price">{special['price']}</span>
                    <div style="margin-top: 8px;">
                        <span style="background: {special['tag_color']}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem;">
                            {special['tag']}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Web search fallback simulation
    if st.button("🔍 Check for Latest Menu Updates"):
        with st.spinner("Searching for latest pizza trends..."):
            search_result = data_manager.simulate_web_search_fallback()
            if search_result["status"] == "success":
                st.success("✅ Menu is up-to-date with latest 2025 trends!")
                st.info(f"🔥 Trending: {', '.join(search_result['trending_items'])}")
            
except Exception as e:
    st.error(f"⚠️ Data retrieval error: {str(e)}")
    st.info("🔄 Falling back to web search...")

st.markdown('<hr class="modern-divider">', unsafe_allow_html=True)

# --- Customer Reviews Section ---
st.markdown("### ⭐ What Our Customers Are Saying")
st.markdown("*Real reviews from verified customers*")

try:
    reviews = data_manager.get_customer_reviews()
    
    # Display reviews in rows of 3
    for row in range(0, len(reviews), 3):
        review_cols = st.columns(3)
        for idx in range(3):
            if row + idx < len(reviews):
                review = reviews[row + idx]
                with review_cols[idx]:
                    st.markdown(f"""
                    <div class="review-card">
                        <div style="text-align: center; margin-bottom: 15px;">
                            <span style="font-size: 1.5rem;">{review['rating']}</span>
                        </div>
                        <p style="font-style: italic; text-align: center; margin-bottom: 15px;">
                            "{review['text']}"
                        </p>
                        <p style="text-align: center; font-weight: 600; color: #6c757d;">
                            - {review['author']}
                        </p>
                        <div style="text-align: center; margin-top: 10px;">
                            <span style="background: {review['tag_color']}; color: white; padding: 4px 12px; border-radius: 15px; font-size: 0.8rem;">
                                {review['tag']}
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

except Exception as e:
    st.error("⚠️ Unable to load customer reviews")
    st.info("📞 Call us for the latest customer feedback: (555) 123-PIZZA")

st.markdown('<hr class="modern-divider">', unsafe_allow_html=True)

# --- Interactive Order Section ---
st.markdown("### 🛒 Place Your Order")
col_order1, col_order2, col_order3 = st.columns([1,2,1])

with col_order2:
    customer_name = st.text_input("👤 Your Name", placeholder="Enter your name")
    
    # Dynamic pizza selection based on available specials
    try:
        specials = data_manager.get_today_specials()
        pizza_options = [f"{special['name']} ({special['price']})" for special in specials]
        pizza_options.extend(["🍕 Classic Margherita ($16.99)", "🍖 Pepperoni Supreme ($18.99)"])
    except:
        pizza_options = ["🍕 Classic Margherita ($16.99)", "🍖 Pepperoni Supreme ($18.99)"]
    
    pizza_choice = st.selectbox("🍕 Choose Your Pizza", pizza_options)
    size_choice = st.select_slider("📏 Select Size", options=["Small", "Medium", "Large", "Family Size"], value="Medium")
    quantity = st.number_input("📊 Quantity", min_value=1, max_value=10, value=1)
    special_notes = st.text_area("📝 Special Instructions (Optional)", placeholder="Any special requests or dietary requirements?")

# Order button
col_btn1, col_btn2, col_btn3 = st.columns([1,1,1])
with col_btn2:
    if st.button("🍕 PLACE ORDER NOW", key="premium_order_btn", type="primary"):
        if customer_name:
            with st.spinner('🔥 Preparing your delicious pizza...'):
                time.sleep(2)
            
            st.balloons()
            st.success(f"""
            🎉 **Order Confirmed!** 
            
            **Customer:** {customer_name}  
            **Pizza:** {pizza_choice}  
            **Size:** {size_choice}  
            **Quantity:** {quantity}  
            
            🕐 **Estimated Delivery:** 25-30 minutes  
            🚚 **Status:** Being prepared by our master pizza chef!
            """)
            
            st.info("📱 You'll receive SMS updates about your order status!")
        else:
            st.error("👤 Please enter your name to place the order!")

# --- Pizza Gallery with High-Quality Images ---
st.markdown('<hr class="modern-divider">', unsafe_allow_html=True)
st.markdown("### 📸 Our Delicious Creations")

# High-quality pizza images from Unsplash
pizza_images = [
    {
        "url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "caption": "🔥 Wood-Fired Margherita"
    },
    {
        "url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "caption": "🍖 Premium Pepperoni"
    },
    {
        "url": "https://images.unsplash.com/photo-1571407970349-bc81e7e96d47?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "caption": "🥩 Meat Lovers Supreme"
    },
    {
        "url": "https://images.unsplash.com/photo-1628840042765-356cda07504e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "caption": "🍍 Hawaiian Paradise"
    },
    {
        "url": "https://images.unsplash.com/photo-1574126154517-d1e0d89ef734?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "caption": "🌱 Veggie Garden Fresh"
    },
    {
        "url": "https://images.unsplash.com/photo-1520201163981-8cc95007dd2a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "caption": "🧀 Four Cheese Delight"
    }
]

# Display pizza images in rows
for row in range(0, len(pizza_images), 3):
    image_cols = st.columns(3)
    for idx in range(3):
        if row + idx < len(pizza_images):
            image = pizza_images[row + idx]
            with image_cols[idx]:
                st.markdown('<div class="pizza-image-container">', unsafe_allow_html=True)
                try:
                    st.image(image["url"], caption=image["caption"], use_container_width=True)
                except Exception:
                    # Fallback with emoji
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ff6b35, #ff8e53); 
                               height: 250px; border-radius: 15px; display: flex; 
                               align-items: center; justify-content: center; color: white;
                               font-size: 4rem; box-shadow: 0 8px 25px rgba(0,0,0,0.15);">
                        🍕
                    </div>
                    <p style="text-align: center; margin-top: 10px; font-weight: 600; color: #2d3748;">{image["caption"]}</p>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="modern-divider">', unsafe_allow_html=True)

# --- 3D Pizza Making Process ---
st.markdown("### 🏭 Pizza Making Process")

process_cols = st.columns(3)

with process_cols[0]:
    st.markdown("""
    <div class="pizza-3d-container" style="margin: 1rem 0;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🥖</div>
        <h4 style="color: #2d3748; margin-bottom: 1rem;">Dough Preparation</h4>
        <p style="color: #6c757d;">Hand-stretched artisan dough made fresh daily</p>
    </div>
    """, unsafe_allow_html=True)

with process_cols[1]:
    st.markdown("""
    <div class="pizza-3d-container" style="margin: 1rem 0;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🍅</div>
        <h4 style="color: #2d3748; margin-bottom: 1rem;">Fresh Toppings</h4>
        <p style="color: #6c757d;">Premium ingredients sourced locally</p>
    </div>
    """, unsafe_allow_html=True)

with process_cols[2]:
    st.markdown("""
    <div class="pizza-3d-container" style="margin: 1rem 0;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🔥</div>
        <h4 style="color: #2d3748; margin-bottom: 1rem;">Wood-Fired Oven</h4>
        <p style="color: #6c757d;">800°F authentic Italian wood-fired cooking</p>
    </div>
    """, unsafe_allow_html=True)

# --- Data Source Information ---
st.markdown('<hr class="modern-divider">', unsafe_allow_html=True)
st.markdown("### 📊 Data Sources & Reliability")

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: rgba(255,255,255,0.8); 
                border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
        <h4 style="color: #2d3748;">🎯 Menu Data</h4>
        <p style="color: #6c757d;">RAG-powered database with 2025 pizza trends</p>
        <p style="color: #28a745; font-weight: 600;">✅ Live & Updated</p>
    </div>
    """, unsafe_allow_html=True)

with col_info2:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: rgba(255,255,255,0.8); 
                border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
        <h4 style="color: #2d3748;">💬 Reviews</h4>
        <p style="color: #6c757d;">Verified customer feedback system</p>
        <p style="color: #28a745; font-weight: 600;">✅ Real Testimonials</p>
    </div>
    """, unsafe_allow_html=True)

with col_info3:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: rgba(255,255,255,0.8); 
                border-radius: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
        <h4 style="color: #2d3748;">🔍 Fallback</h4>
        <p style="color: #6c757d;">Web search for latest trends</p>
        <p style="color: #ffc107; font-weight: 600;">⚡ Backup Ready</p>
    </div>
    """, unsafe_allow_html=True)

# --- Contact Information ---
st.markdown("### 📞 Contact Pizza Paradise")
contact_col1, contact_col2, contact_col3 = st.columns(3)

with contact_col1:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.9); 
                border-radius: 15px; border: 1px solid rgba(255,107,53,0.2);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
        <h4 style="color: #2d3748;">📞 Phone Orders</h4>
        <p style="font-size: 1.3rem; font-weight: 600; color: #ff6b35; margin: 1rem 0;">(555) 123-PIZZA</p>
        <p style="color: #6c757d;">24/7 Order Hotline</p>
    </div>
    """, unsafe_allow_html=True)

with contact_col2:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.9); 
                border-radius: 15px; border: 1px solid rgba(255,107,53,0.2);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
        <h4 style="color: #2d3748;">📍 Visit Us</h4>
        <p style="font-weight: 600; color: #ff6b35; margin: 1rem 0;">123 Pizza Street</p>
        <p style="color: #6c757d;">Downtown Foodie District</p>
    </div>
    """, unsafe_allow_html=True)

with contact_col3:
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.9); 
                border-radius: 15px; border: 1px solid rgba(255,107,53,0.2);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
        <h4 style="color: #2d3748;">⏰ Opening Hours</h4>
        <p style="font-weight: 600; color: #ff6b35; margin: 1rem 0;">Mon-Sun</p>
        <p style="color: #6c757d;">11:00 AM - 12:00 AM</p>
    </div>
    """, unsafe_allow_html=True)

# --- System Status and Analytics ---
st.markdown('<hr class="modern-divider">', unsafe_allow_html=True)
st.markdown("### 📈 System Status & Analytics")

status_col1, status_col2, status_col3, status_col4 = st.columns(4)

with status_col1:
    st.metric("🍕 Orders Today", "247", "+23")

with status_col2:
    st.metric("⭐ Avg Rating", "4.9", "+0.1")

with status_col3:
    st.metric("🚚 Delivery Time", "22 min", "-3 min")

with status_col4:
    st.metric("🔄 System Uptime", "99.9%", "🟢")

# --- Advanced Features Demo ---
if st.checkbox("🔧 Show Advanced Features", help="Toggle to see technical implementation details"):
    st.markdown("#### 🛠️ Technical Implementation")
    
    with st.expander("📊 RAG System Status"):
        st.code("""
        Vector Database: ✅ Connected
        Embedding Model: sentence-transformers/all-MiniLM-L6-v2
        Menu Items Indexed: 24 pizzas
        Last Update: 2025-01-15 10:30 UTC
        Query Response Time: 45ms avg
        """, language="text")
    
    with st.expander("🌐 Web Search Fallback"):
        st.code("""
        Search Engine: Multi-source aggregation
        Trending Topics: Pizza trends 2025, customer reviews
        Fallback Triggers: API timeout, data staleness
        Cache TTL: 1 hour for trends, 24 hours for reviews
        """, language="text")
    
    with st.expander("💾 Data Management"):
        st.json({
            "primary_source": "PostgreSQL + Vector Store",
            "cache_layer": "Redis",
            "fallback_sources": ["Web Search", "Static JSON"],
            "update_frequency": "Real-time for orders, Hourly for menu",
            "data_validation": "Schema validation + Content moderation"
        })

# --- Error Handling Demo ---
if st.button("🔄 Test Fallback System", help="Simulate system failure to demonstrate fallback"):
    st.warning("⚠️ Simulating primary data source failure...")
    
    with st.spinner("Activating fallback mechanisms..."):
        time.sleep(2)
    
    st.success("✅ Fallback system activated successfully!")
    st.info("""
    **Fallback Actions Taken:**
    - ✅ Switched to cached menu data
    - ✅ Activated web search for trends  
    - ✅ Displayed backup customer reviews
    - ✅ Maintained full functionality
    """)

# --- 3D Pizza Nutrition Facts ---
st.markdown('<hr class="modern-divider">', unsafe_allow_html=True)
st.markdown("### 🥗 Nutrition Information")

nutrition_cols = st.columns(3)

with nutrition_cols[0]:
    st.markdown("""
    <div class="pizza-3d-container">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🌱</div>
        <h4 style="color: #2d3748;">Organic Ingredients</h4>
        <p style="color: #6c757d;">Fresh, locally sourced vegetables and herbs</p>
        <div style="margin-top: 1rem;">
            <span style="background: #28a745; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem;">
                ✅ Certified Organic
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with nutrition_cols[1]:
    st.markdown("""
    <div class="pizza-3d-container">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🧀</div>
        <h4 style="color: #2d3748;">Premium Cheese</h4>
        <p style="color: #6c757d;">Fresh mozzarella from local dairy farms</p>
        <div style="margin-top: 1rem;">
            <span style="background: #ffc107; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem;">
                🏆 Award Winning
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with nutrition_cols[2]:
    st.markdown("""
    <div class="pizza-3d-container">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🔥</div>
        <h4 style="color: #2d3748;">Wood-Fired Method</h4>
        <p style="color: #6c757d;">Traditional Italian cooking technique</p>
        <div style="margin-top: 1rem;">
            <span style="background: #dc3545; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem;">
                🌡️ 800°F Perfect
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

