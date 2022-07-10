mkdir -p ~/.streamlit/
echo "[theme]
primaryColor='#1d4289'
backgroundColor='#FFFFFF'
secondaryBackgroundColor='#F0F2F6'
font = 'sans serif'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml