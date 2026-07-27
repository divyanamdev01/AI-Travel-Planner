import streamlit as st
from dotenv import load_dotenv
from services.travel_planner import create_trip_plan
from services.image_service import get_place_image
from utils.usage_limit import (
     initialize_usage,
     can_use,
     increase_usage,
     remaining_uses
)


load_dotenv()

st.set_page_config(
    page_title='AI Travel Planner',
    page_icon="✈️")

initialize_usage()

st.title("🌍 AI Travel Planner")
st.write('Plan your trip with AI ✈️')


# show remaining uses
remaining= remaining_uses()
        
if remaining>0:
      st.info(f"🎟️ You have {remaining} trip planning attempt(s) remaining.")
else :
    st.error(
        "🚫 You have used all 2 free trip planning attempts."
    )
    st.stop()
          
location=st.text_input('📍 Enter Location:')
if st.button('🚀 Plan My Trip'):
        if location.strip()=='':
                st.warning('please enter a location')    
        elif not can_use():
             st.error(
            "🚫 You have reached the maximum limit of 2 uses."
        )
        else:     
            with st.spinner('planning you trip...'):
                    result = create_trip_plan(location)

            # Gemini token/quota complete
            if result.get('error')=='TOKEN_LIMIT':
                  st.error("" 
                        "⚠️ AI service token/quota limit has been reached. "
                        "Please try again later."
                  "")   

            
            elif "error" in result:

                st.error(
                    f"❌ Something went wrong: {result['error']}"
                )

            else:
                 #count only successful trip generation
                increase_usage()

                places = result["places"]
                hotels = result["hotels"]
                itinerary = result["itinerary"]
                budget = result["budget"]
                tips = result["tips"]

                # Tourist Places
                st.subheader("📍 Tourist Places")

                cols=st.columns(3)
                places_list=places.split('\n')[:6]


                for i,place in enumerate(places_list):
                    with cols[i%3]:
                        img_url=get_place_image(place)
                        if img_url:
                            st.image(
                                img_url, 
                                width='stretch',
                                use_container_width=True)
                        st.markdown(f'###{place}')
                st.divider()
                st.subheader('🏨Hotels')
                st.write(hotels)

                st.subheader("🗒️Itnerary")        
                st.write( itinerary)

                st.subheader("💰Budget")
                st.write(budget)

                st.subheader("💡Travel Tips")
                st.write(tips)
                st.success('✅ Trip Planning Successfully Done !')

                 # Show remaining attempts
                remaining = remaining_uses()

                if remaining > 0:
                    st.info(
                        f"🎟️ You have {remaining} attempt remaining."
                    )
                else:
                    st.warning(
                        "🚫 You have used both of your free attempts."
                    )