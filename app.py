import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="OctoPi", page_icon="🐙", layout="wide")

def get_img_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

# octo_b64 = get_img_base64("octopus.png")
# octo_src = f"data:image/png;base64,{octo_b64}" if octo_b64 else ""


bg_top, bg_mid, bg_bot   = "#061a2e", "#0a2f52", "#0e4a7a"
seabed_color             = "#2a1d12"
sand_color               = "#5a3e24"
text_color               = "#E8F4FD"
sub_color                = "#90b8d8"
seaweed1                 = "#1a6b3c"
seaweed2                 = "#22884d"
rock_color               = "#2c3e50"
fish_opacity             = 0.55

st.markdown(f"""
<style>
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"] {{ display: none !important; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    .stApp {{
        background: linear-gradient(180deg, {bg_top} 0%, {bg_mid} 55%, {bg_bot} 100%);
        overflow: hidden;
    }}
    .stMainBlockContainer, .block-container {{ padding: 0 !important; max-width: 100% !important; }}
    [data-testid="stButton"] > button {{
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 50px !important;
        color: {text_color} !important;
        font-size: 20px !important;
        width: 48px !important; height: 48px !important;
        padding: 0 !important; min-height: unset !important;
        position: fixed; top: 16px; right: 20px; z-index: 9999;
        backdrop-filter: blur(8px);
        transition: transform 0.2s;
    }}
    [data-testid="stButton"] > button:hover {{ transform: scale(1.12) !important; }}
</style>
""", unsafe_allow_html=True)

scene_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    width: 100vw; 
    height: 100vh;
    overflow: hidden;
    background: transparent;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }}
  
  html, body {{
    height: 100vh; 
  }}

  /* -- Animations -- */
  @keyframes bobbing {{
    0%,100% {{ transform: translateY(0px) rotate(-1.5deg); }}
    50%      {{ transform: translateY(-22px) rotate(1.5deg); }}
  }}
  @keyframes sway {{
    0%,100% {{ transform: rotate(-9deg); }}
    50%     {{ transform: rotate(9deg); }}
  }}
  @keyframes rise {{
    0%   {{ bottom:-60px; opacity:.75; }}
    100% {{ bottom:110vh;  opacity:0;  }}
  }}
  @keyframes popIn {{
    0%  {{ transform:scale(0.4); opacity:0; }}
    70% {{ transform:scale(1.1); }}
    100%{{ transform:scale(1);   opacity:1; }}
  }}
  @keyframes swimLeft {{
    0%   {{ right:-150px; }}
    100% {{ right:130vw;  }}
  }}
  @keyframes swimRight {{
    0%   {{ left:-150px; }}
    100% {{ left:130vw;  }}
  }}
  @keyframes pulse {{
    0%,100% {{ box-shadow: 0 8px 30px rgba(245,230,66,.4); }}
    50%     {{ box-shadow: 0 8px 48px rgba(245,230,66,.7); }}
  }}

  /* -- Bubbles -- */
  .bubble {{
    position: fixed;
    border-radius: 50%;
    background: rgba(255,255,255,.15);
    border: 1.5px solid rgba(255,255,255,.3);
    animation: rise linear infinite;
  }}

  /* -- Seaweed -- */
  .seaweed {{
    position: fixed; 
    bottom: 40px;
    transform-origin: bottom center;
    animation: sway ease-in-out infinite;
    z-index: 3;
  }}

  /* -- Fish -- */
  .fish {{
    position: fixed;
    opacity: {fish_opacity};
    filter: drop-shadow(0 2px 6px rgba(0,0,0,.25));
    z-index: 1;
    will-change: transform;
  }}
  .fish-l {{ animation: swimLeft linear infinite; }}
  .fish-r {{ animation: swimRight linear infinite; transform: scaleX(-1); }}

  /* -- Rocks -- */
  .rock {{
    position: fixed;
    bottom: 5px;
    width: 50px;
    height: 30px;
    background: {rock_color};
    border-radius: 40% 60% 40% 40%;
    z-index: 6;
    filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.4));
    transform: rotate(var(--r, 0deg));
    }}
  
  /* -- Coral  -- */
  .coral {{
    position: fixed; 
    bottom: 70px;
    opacity: 0.9;
    z-index: 3; 
  }}

  /* -- Seabed -- */
  .seabed {{
    position: fixed; 
    bottom: 0; 
    left: 0;
    width: 100vw; 
    height: 110px;
    background: {seabed_color};
    border-top: 3px solid rgba(0,0,0,0.3);
    border-radius: 60% 60% 0 0 / 30px 30px 0 0;
    z-index: 2;
    opacity: 1;
    filter: none;
  }}
  .seabed::before {{
    content: '';
    position: absolute; 
    top: -18px; 
    left: 0;
    width:100%; 
    height:36px;
    background: {sand_color};
    border-radius: 50%;
    filter: blur(6px);
    opacity: 0.7;
  }}

  /* -- Center stack: octo → title → sub → button -- */
  .center-stack {{
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    z-index: 10;
    /* push it up slightly so it clears the seabed */
    margin-top: -40px;
  }}

  /* Octopus wrapper */
  .octo-wrap {{
    position: relative;
    width: clamp(160px, 20vw, 280px);
    animation: bobbing 4s ease-in-out infinite;
  }}
  # .octo-wrap img {{
  #   width:100%;
  #   filter: drop-shadow(0 16px 40px rgba(0,0,0,.3));
  # }}

  /* Speech bubble — sits top-right of the octo box */
  .speech {{
    position: absolute;
    top: -14px;
    right: -160px;
    background: white;
    color: #222;
    padding: 9px 16px;
    border-radius: 18px;
    font-size: clamp(12px, 1vw, 14px);
    font-weight: 700;
    white-space: nowrap;
    box-shadow: 0 4px 18px rgba(0,0,0,.18);
    animation: popIn .5s cubic-bezier(.34,1.56,.64,1) 1s both;
  }}
  .speech::after {{
    content:'';
    position:absolute;
    bottom:-10px; left:22px;
    border:10px solid transparent;
    border-top-color:white;
    border-bottom:0;
  }}
  .octo-svg {{
    width: 100%;
    filter: drop-shadow(0 16px 40px rgba(0,0,0,0.3));
  }}
  .arm {{
    transform-origin: top;
    animation: wave 2.5s ease-in-out infinite; 
  }}

  .arm.delay {{
    animation-delay: 0.4s; 
  }}

  @keyframes wave {{
    0%   {{ transform: rotate(-8deg) scaleY(1); }}
    40%  {{ transform: rotate(6deg) scaleY(1.05); }}
    70%  {{ transform: rotate(2deg) scaleY(0.98); }}
    100% {{ transform: rotate(-8deg) scaleY(1); }}
  }}  

  /* Title */
  .hero-title {{
    color: {text_color};
    font-size: clamp(44px, 6vw, 76px);
    font-weight: 900;
    letter-spacing: -1.5px;
    margin: 14px 0 6px;
    text-shadow: 0 4px 28px rgba(0,0,0,.22);
    text-align: center;
  }}
  .hero-sub {{
    color: {sub_color};
    font-size: clamp(14px, 1.3vw, 17px);
    font-weight: 500;
    margin-bottom: 28px;
    text-align: center;
  }}
  .dive-btn {{
    background: rgba(255,255,255,0.08); 
    color: #E8F4FD;
    font-weight: 700;
    border-radius: 50px;
    padding: 14px 56px;
    border: 1px solid rgba(255,255,255,0.18);
    font-size: clamp(15px, 1.2vw, 17px);
    cursor: pointer;
    transition: all 0.25s ease;
    text-decoration: none;
    display: inline-block;
    box-shadow: 0 6px 20px rgba(158, 62, 26, 0.25)
    backdrop-filter: blur(10px);
  }}
  .dive-btn:hover {{ 
    transform: translateY(-3px) scale(1.04);
    box-shadow: 0 12px 35px rgba(158, 62, 26, 0.4); }}
</style>
</head>
<body>

<!--  Bubbles  -->
<div class="bubble" style="width:9px;height:9px;left:5vw;animation-duration:8s;animation-delay:0s;bottom:-60px;"></div>
<div class="bubble" style="width:15px;height:15px;left:12vw;animation-duration:11s;animation-delay:1.3s;bottom:-60px;"></div>
<div class="bubble" style="width:7px;height:7px;left:20vw;animation-duration:9s;animation-delay:2.6s;bottom:-60px;"></div>
<div class="bubble" style="width:19px;height:19px;left:32vw;animation-duration:13s;animation-delay:0.9s;bottom:-60px;"></div>
<div class="bubble" style="width:11px;height:11px;left:47vw;animation-duration:10s;animation-delay:3.1s;bottom:-60px;"></div>
<div class="bubble" style="width:8px;height:8px;left:58vw;animation-duration:8.5s;animation-delay:1.7s;bottom:-60px;"></div>
<div class="bubble" style="width:17px;height:17px;left:68vw;animation-duration:12s;animation-delay:0.5s;bottom:-60px;"></div>
<div class="bubble" style="width:10px;height:10px;left:78vw;animation-duration:9.5s;animation-delay:2.2s;bottom:-60px;"></div>
<div class="bubble" style="width:13px;height:13px;left:87vw;animation-duration:11.5s;animation-delay:1.1s;bottom:-60px;"></div>
<div class="bubble" style="width:6px;height:6px;left:93vw;animation-duration:7.5s;animation-delay:3.8s;bottom:-60px;"></div>
<div class="bubble" style="width:14px;height:14px;left:40vw;animation-duration:10.5s;animation-delay:0.3s;bottom:-60px;"></div>
<div class="bubble" style="width:8px;height:8px;left:25vw;animation-duration:9.8s;animation-delay:4s;bottom:-60px;"></div>

<!--  Fish swimming in background   -->
<!-- Small fish going left (RTL) at different heights -->
<svg class="fish fish-l" style="bottom:38vh;animation-duration:18s;animation-delay:0s;width:60px;" viewBox="0 0 60 30" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="28" cy="15" rx="20" ry="9" fill="#5bb8d4" opacity=".8"/>
  <polygon points="48,15 60,6 60,24" fill="#5bb8d4" opacity=".8"/>
  <circle cx="12" cy="12" r="3" fill="white"/>
  <circle cx="11" cy="11" r="1.5" fill="#1a3a4a"/>
</svg>
<svg class="fish fish-l" style="bottom:55vh;animation-duration:24s;animation-delay:4s;width:42px;" viewBox="0 0 60 30" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="28" cy="15" rx="20" ry="9" fill="#f4a460" opacity=".7"/>
  <polygon points="48,15 60,6 60,24" fill="#f4a460" opacity=".7"/>
  <circle cx="12" cy="12" r="3" fill="white"/>
  <circle cx="11" cy="11" r="1.5" fill="#5a2a00"/>
</svg>
<svg class="fish fish-l" style="bottom:25vh;animation-duration:30s;animation-delay:10s;width:35px;" viewBox="0 0 60 30" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="28" cy="15" rx="20" ry="9" fill="#a78bfa" opacity=".65"/>
  <polygon points="48,15 60,6 60,24" fill="#a78bfa" opacity=".65"/>
  <circle cx="12" cy="12" r="3" fill="white"/>
  <circle cx="11" cy="11" r="1.5" fill="#2a1a4a"/>
</svg>

<!-- Fish going right (LTR) -->
<svg class="fish fish-r" style="bottom:44vh;animation-duration:22s;animation-delay:7s;width:50px;" viewBox="0 0 60 30" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="28" cy="15" rx="20" ry="9" fill="#34d399" opacity=".65"/>
  <polygon points="48,15 60,6 60,24" fill="#34d399" opacity=".65"/>
  <circle cx="12" cy="12" r="3" fill="white"/>
  <circle cx="11" cy="11" r="1.5" fill="#064e3b"/>
</svg>
<svg class="fish fish-r" style="bottom:62vh;animation-duration:28s;animation-delay:2s;width:38px;" viewBox="0 0 60 30" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="28" cy="15" rx="20" ry="9" fill="#fb923c" opacity=".6"/>
  <polygon points="48,15 60,6 60,24" fill="#fb923c" opacity=".6"/>
  <circle cx="12" cy="12" r="3" fill="white"/>
  <circle cx="11" cy="11" r="1.5" fill="#5a1a00"/>
</svg>

<!-- Seaweed along seabed -->
<div class="seaweed" style="left:3vw;animation-duration:3.2s;">
  <svg width="50" height="150" viewBox="0 0 50 150" fill="none"><path d="M25 150 Q5 122 25 94 Q45 66 25 38 Q5 14 18 0" stroke="{seaweed1}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M25 120 Q45 100 38 80" stroke="{seaweed2}" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M25 80 Q5 65 14 46" stroke="{seaweed2}" stroke-width="3.5" fill="none" stroke-linecap="round"/></svg>
</div>
<div class="seaweed" style="left:8vw;animation-duration:4s;animation-delay:.7s;">
  <svg width="36" height="115" viewBox="0 0 36 115" fill="none"><path d="M18 115 Q2 93 18 70 Q34 47 18 24 Q4 6 13 0" stroke="{seaweed1}" stroke-width="6" fill="none" stroke-linecap="round"/></svg>
</div>
<div class="seaweed" style="left:14vw;animation-duration:3.7s;animation-delay:1.2s;">
  <svg width="30" height="90" viewBox="0 0 30 90" fill="none"><path d="M15 90 Q2 72 15 54 Q28 36 15 18 Q4 4 11 0" stroke="{seaweed2}" stroke-width="5" fill="none" stroke-linecap="round"/></svg>
</div>
<div class="seaweed" style="left:20vw;animation-duration:3.4s;animation-delay:.3s;">
  <svg width="44" height="130" viewBox="0 0 44 130" fill="none"><path d="M22 130 Q4 106 22 82 Q40 58 22 34 Q4 12 16 0" stroke="{seaweed1}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M22 100 Q40 82 33 62" stroke="{seaweed2}" stroke-width="3.5" fill="none" stroke-linecap="round"/></svg>
</div>
<div class="seaweed" style="right:3vw;animation-duration:3.9s;animation-delay:.5s;">
  <svg width="48" height="145" viewBox="0 0 48 145" fill="none"><path d="M24 145 Q4 118 24 91 Q44 64 24 37 Q4 14 17 0" stroke="{seaweed1}" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M24 115 Q44 95 36 75" stroke="{seaweed2}" stroke-width="4" fill="none" stroke-linecap="round"/></svg>
</div>
<div class="seaweed" style="right:8vw;animation-duration:3.1s;animation-delay:1.6s;">
  <svg width="34" height="105" viewBox="0 0 34 105" fill="none"><path d="M17 105 Q2 84 17 63 Q32 42 17 21 Q4 5 12 0" stroke="{seaweed1}" stroke-width="5" fill="none" stroke-linecap="round"/></svg>
</div>
<div class="seaweed" style="right:14vw;animation-duration:4.2s;animation-delay:.9s;">
  <svg width="28" height="88" viewBox="0 0 28 88" fill="none"><path d="M14 88 Q1 70 14 52 Q27 34 14 16 Q3 3 10 0" stroke="{seaweed2}" stroke-width="4.5" fill="none" stroke-linecap="round"/></svg>
</div>
<div class="seaweed" style="right:20vw;animation-duration:3.5s;animation-delay:2s;">
  <svg width="40" height="120" viewBox="0 0 40 120" fill="none"><path d="M20 120 Q3 97 20 74 Q37 51 20 28 Q5 8 15 0" stroke="{seaweed1}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M20 95 Q37 77 30 58" stroke="{seaweed2}" stroke-width="3.5" fill="none" stroke-linecap="round"/></svg>
</div>

<div class="seaweed" style="left:25vw;animation-duration:3.6s;animation-delay:1s;">
  <svg width="40" height="120" viewBox="0 0 40 120" fill="none">
    <path d="M20 120 Q3 97 20 74 Q37 51 20 28 Q5 8 15 0" stroke="{seaweed1}" stroke-width="6" fill="none" stroke-linecap="round"/>
  </svg>
</div>

<div class="seaweed" style="left:32vw;animation-duration:4.2s;">
  <svg width="30" height="100" viewBox="0 0 30 100" fill="none">
    <path d="M15 100 Q2 80 15 60 Q28 40 15 20 Q4 5 10 0" stroke="{seaweed2}" stroke-width="5" fill="none" stroke-linecap="round"/>
  </svg>
</div>

<div class="seaweed" style="right:25vw;animation-duration:3.8s;">
  <svg width="36" height="110" viewBox="0 0 36 110" fill="none">
    <path d="M18 110 Q2 88 18 66 Q34 44 18 22 Q4 6 12 0" stroke="{seaweed1}" stroke-width="6" fill="none" stroke-linecap="round"/>
  </svg>
</div>

<div class="seaweed" style="right:32vw;animation-duration:4.1s;animation-delay:.6s;">
  <svg width="28" height="90" viewBox="0 0 28 90" fill="none">
    <path d="M14 90 Q1 70 14 50 Q27 30 14 10 Q3 3 9 0" stroke="{seaweed2}" stroke-width="4.5" fill="none" stroke-linecap="round"/>
  </svg>
</div>

<! -- Rocks --> 
<div class="rock" style="left:10vw; width:60px; height:35px --r:12deg;"></div>
<div class="rock" style="left:18vw; width:40px; height:25px; --r:8deg"></div>
<div class="rock" style="right:12vw; width:80px; height:45px;"></div>
<div class="rock" style="right:22vw; width:50px; height:30px;"></div>

<! -- Coral -->
<div class="coral" style="left:6vw;">
  <svg width="80" height="120" viewBox="0 0 80 120">
    <path d="M40 120 Q20 90 40 60 Q60 30 30 10" stroke="#ff7f50" stroke-width="8" fill="none" stroke-linecap="round"/>
    <path d="M40 80 Q65 60 55 30" stroke="#ff9966" stroke-width="6" fill="none" stroke-linecap="round"/>
    <path d="M40 60 Q15 45 25 20" stroke="#ffb347" stroke-width="5" fill="none" stroke-linecap="round"/>
  </svg>
</div>

<div class="coral" style="right:6vw;">
  <svg width="80" height="120" viewBox="0 0 80 120">
    <path d="M40 120 Q60 90 40 60 Q20 30 50 10" stroke="#ff6b6b" stroke-width="8" fill="none" stroke-linecap="round"/>
    <path d="M40 80 Q20 60 30 35" stroke="#ff8787" stroke-width="6" fill="none" stroke-linecap="round"/>
  </svg>
</div>

<div class="coral" style="right:6vw;">
  <svg width="60" height="100" viewBox="0 0 60 100">
    <path d="M30 100 Q40 70 30 50 Q20 30 35 10" stroke="#ff6b6b" stroke-width="6" fill="none" stroke-linecap="round"/>
  </svg>
</div>

<!--  Seabed  -->
<div class="seabed"></div>

<!-- Center stack: octopus → title → sub → button -->
<div class="center-stack">

  <!-- Octopus + speech bubble as a relative unit -->
  <svg class="octo-svg" viewBox="0 0 200 220">
  <style>
    .arm {{ transform-origin: 50% 0%; animation: wave 2.8s ease-in-out infinite; }}
    .arm.d1 {{ animation-delay: 0.2s; }}
    .arm.d2 {{ animation-delay: 0.5s; }}
    .arm.d3 {{ animation-delay: 0.8s; }}
    .arm.d4 {{ animation-delay: 1.1s; }}
    .arm.d5 {{ animation-delay: 1.4s; }}
    .arm.d6 {{ animation-delay: 1.7s; }}
    
    @keyframes wave {{
      0%,100% {{ transform: rotate(-12deg) scaleY(1); }}
      50%      {{ transform: rotate(12deg) scaleY(1.06); }}
    }}
  
  </style>

  <!-- Tentacles (behind head) -->
  <path class="arm d1" d="M68 148 C52 162, 42 178, 50 195 C55 205, 65 205, 66 195" stroke="#c95530" stroke-width="9" fill="none" stroke-linecap="round"/>
  <path class="arm d2" d="M78 152 C65 168, 60 185, 68 198 C73 206, 82 204, 82 194" stroke="#c95530" stroke-width="9" fill="none" stroke-linecap="round"/>
  <path class="arm d3" d="M90 155 C83 172, 82 190, 90 200 C94 206, 101 204, 100 196" stroke="#c95530" stroke-width="9" fill="none" stroke-linecap="round"/>
  <path class="arm d4" d="M100 156 C100 174, 100 192, 100 202" stroke="#c95530" stroke-width="9" fill="none" stroke-linecap="round"/>
  <path class="arm d5" d="M110 155 C117 172, 118 190, 110 200 C106 206, 99 204, 100 196" stroke="#c95530" stroke-width="9" fill="none" stroke-linecap="round"/>
  <path class="arm d6" d="M122 152 C135 168, 140 185, 132 198 C127 206, 118 204, 118 194" stroke="#c95530" stroke-width="9" fill="none" stroke-linecap="round"/>
  <path class="arm"   d="M132 148 C148 162, 158 178, 150 195 C145 205, 135 205, 134 195" stroke="#c95530" stroke-width="9" fill="none" stroke-linecap="round"/>

  <!-- Body (fills gap between mantle and tentacles) -->
  <rect x="58" y="68" width="84" height="70" fill="#e0703a" rx="2"/>
  <ellipse cx="100" cy="135" rx="42" ry="30" fill="#e0703a"/>

  <!-- Mantle dome -->
  <ellipse cx="100" cy="70" rx="44" ry="50" fill="#e0703a"/>
  <ellipse cx="88" cy="50" rx="18" ry="24" fill="#eb8a54" opacity="0.35"/>

  <!-- Eyes -->
  <circle cx="83" cy="78" r="12" fill="white"/>
  <circle cx="117" cy="78" r="12" fill="white"/>
  <circle cx="85" cy="80" r="7" fill="#1a1a2e"/>
  <circle cx="119" cy="80" r="7" fill="#1a1a2e"/>
  <circle cx="87" cy="77" r="2.5" fill="white"/>
  <circle cx="121" cy="77" r="2.5" fill="white"/>

  <!-- Smile + blush -->
  <path d="M88 100 Q100 112 112 100" stroke="#b8501f" stroke-width="3.5" fill="none" stroke-linecap="round"/>
  <ellipse cx="72" cy="94" rx="8" ry="5" fill="#f4a07a" opacity="0.5"/>
  <ellipse cx="128" cy="94" rx="8" ry="5" fill="#f4a07a" opacity="0.5"/>
  
  </svg>

  <div class="speech">Hi there! 👋 Ready to study?</div>
  </div>

  <div class="hero-title">OctoPi</div>
  <div class="hero-sub">Your free, unlimited AI study buddy</div>
  <a href="/study" target="_self" class="dive-btn">Dive in 🌊</a>

</div>

</body>
</html>
"""

components.html(scene_html, height=930, scrolling=False)


