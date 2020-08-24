mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"joao@ice.ufjf.br\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml