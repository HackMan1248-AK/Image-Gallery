import streamlit as st
import requests, json # ! For Unsplash API

class UnsplashApp:
    def __init__(self):
        self.access_key = "UH6x10uJMjl5XrYT1ChKXWKw-kX8JP9k5tXBHPWyBBM"
        self.image_urls = []
    
    def get_images(self, category, amount=10):
        url = f"https://api.unsplash.com/photos/random?client_id={self.access_key}&query={category}&count={amount}"
        response = requests.get(url) # * Get the response

        try: data = response.json()
        except json.JSONDecodeError:
            print("Please check you connection or try again later.")
            return []
        
        return data
    
    def download_image(self, image_url):
        response = requests.get(image_url)
        return response.content

def main():
    # * Give Title to website
    st.write("# Image Gallery")
    unsplash = UnsplashApp() # * Object of class for Unsplash
    col1, col2 = st.columns([0.5, 0.5]) # * Created columns for creating boxes that are side by side.
    with col1:
        selected_category = st.selectbox("Select a category", ["Urban", "Nature", "Culture", "Wildlife", "Art"], on_change=lambda: st.session_state.update({"search": ""})) # * Dropdown Select

    with col2:
        custom_category = st.text_input("Search for a custom category:", key="search") # * Search Select

    amount = st.slider("Select amount of images:", min_value=3, max_value=30, value=6, step=3)

    if custom_category: # * IF the user has searched for a specific category
        gallery = unsplash.get_images(custom_category, amount)
    elif selected_category: # * IF the user has selected a specific category
        gallery = unsplash.get_images(selected_category, amount)
    
    for i in range(0, len(gallery), 3):
        cols = st.columns(3)
        for j, image in enumerate(gallery[i:i+3]):
            image_url = image["urls"]["regular"]
            cols[j].image(image_url)
            image_data = unsplash.download_image(image_url)
            st.download_button(f"Download {i + 1}", image_data, file_name=f"image_{i + 1}.jpg", mime="image/jpeg")
            open_in_new_tab_button = f"""
                <a href="{image_url}" target="_blank">
                    <button class="custom-button">Open Image {i + 1} in New Tab</button>
                </a>
            """
            st.markdown(open_in_new_tab_button, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
