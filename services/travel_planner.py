from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def create_trip_plan(location):

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash"
        )

        # Tourist Places
        place_prompt = ChatPromptTemplate.from_template("""
                    List only the top 6 tourist places in {location}.
                    Return only place names as bullet points.
                    """)

        place_chain = place_prompt | llm | StrOutputParser()

        # Hotels
        hotel_prompt = ChatPromptTemplate.from_template(
            """
                Suggest only 3 good hotels in {location}.
                Return only hotel names with one short line.
                """  )

        hotel_chain = hotel_prompt | llm | StrOutputParser()

        # Itinerary
        itinerary_prompt = ChatPromptTemplate.from_template("""
                            Create a concise 3-day itinerary using these places:
                            
                            {places}
                            
                            Rules:
                            - Cover all places.
                            - Maximum 4 bullet points per day.
                            - Keep the response under 250 words.
                            """  )

        itinerary_chain = itinerary_prompt | llm | StrOutputParser()

        # Budget
        budget_prompt = ChatPromptTemplate.from_template("""
                            Estimate the budget for a 3-day trip to {location}.
                            
                            Include:
                            - Hotel
                            - Food
                            - Local Transport
                            - Entry Tickets
                            - Total Estimated Cost
                            
                            Keep the response under 100 words.
                            """)

        budget_chain = budget_prompt | llm | StrOutputParser()

        # Travel Tips
        tips_prompt = ChatPromptTemplate.from_template(
           """
                    Give 5 short travel tips for {location}.
                    
                    Rules:
                    - One line per tip.
                    - No explanation.
                    - Keep the total response under 80 words.
                    """
        )

        tips_chain = tips_prompt | llm | StrOutputParser()

        # Invoke
        places = place_chain.invoke({
            "location": location
        })

        hotels = hotel_chain.invoke({
            "location": location
        })

        itinerary = itinerary_chain.invoke({
            "places": places
        })

        budget = budget_chain.invoke({
            "itinerary": itinerary
        })

        tips = tips_chain.invoke({
            "location": location
        })

        return {
            "places": places,
            "hotels": hotels,
            "itinerary": itinerary,
            "budget": budget,
            "tips": tips
        }

    except Exception as e:

        error_message = str(e).lower()

        if (
            "resource_exhausted" in error_message
            or "quota" in error_message
            or "429" in error_message
            or "rate limit" in error_message
        ):
            return {
                "error": "TOKEN_LIMIT"
            }

        return {
            "error": str(e)
        }
