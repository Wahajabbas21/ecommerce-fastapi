import os
from google import genai
from google.genai import types
from app.core.config import get_settings
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product 
from app.models.order import Order

settings = get_settings()

def get_ai_tools(db: Session, user_id: int):
    """Factory function to create product and order search tools securely bound to a database session and authenticated user ID."""
    
    def search_products(query: str) -> str:
        """Search for products in the live store database based on keyword, name, or category.
        
        Args:
            query: The search term like shirt, jeans, shoes, watch, laptop, etc.
        """
        try:
            products = db.query(Product).filter(
                (Product.name.ilike(f"%{query}%")) | 
                (Product.description.ilike(f"%{query}%"))
            ).all()
            
            if not products:
                return "No products found matching your query in our inventory."
            
            result_list = []
            for p in products:
                result_list.append({
                    "name": p.name,
                    "price": f"{p.price} PKR",
                    "stock": "Available" if p.stock > 0 else "Out of Stock",
                    "description": p.description
                })
            return str(result_list)
        except Exception as e:
            return f"Database search error: {str(e)}"

    def get_my_orders() -> str:
        """Retrieve all orders placed by the currently authenticated customer."""
        try:
            orders = db.query(Order).filter(Order.user_id == user_id).all()
            if not orders:
                return "You have not placed any orders yet."
            
            result_list = []
            for o in orders:
                result_list.append({
                    "order_id": o.id,
                    "total_price": f"{o.total_price} PKR",
                    "status": o.status,
                    "created_at": str(o.created_at)
                })
            return str(result_list)
        except Exception as e:
            return f"Error fetching orders: {str(e)}"

    def get_latest_order() -> str:
        """Retrieve the most recent order placed by the authenticated customer[cite: 4]."""
        try:
            order = db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).first()
            if not order:
                return "No recent orders found for your account."
            
            return str({
                "order_id": order.id,
                "total_price": f"{order.total_price} PKR",
                "status": order.status,
                "created_at": str(order.created_at)
            })
        except Exception as e:
            return f"Error fetching latest order: {str(e)}"

    def get_order_status(order_id: int) -> str:
        """Check the status of a specific order belonging to the authenticated customer by its ID[cite: 4].
        
        Args:
            order_id: The ID of the order to check.
        """
        try:
            order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
            if not order:
                return f"Order with ID {order_id} was not found under your account."
            
            return f"Order #{order.id} status is currently: {order.status}."
        except Exception as e:
            return f"Error checking order status: {str(e)}"

    return [search_products, get_my_orders, get_latest_order, get_order_status]

class AIService:
    @staticmethod
    async def generate_chat_response(prompt: str, db: Session, user_id: int) -> str:
        if not settings.ai_api_key:
            raise HTTPException(status_code=500, detail="AI service key is not configured.")
        
        try:
            os.environ["GEMINI_API_KEY"] = settings.ai_api_key
            client = genai.Client()
            
            # Bind live database session and authenticated user ID securely to all tools[cite: 4]
            tools = get_ai_tools(db, user_id)
            
            chat = client.chats.create(
                model=settings.ai_model_name,
                config=types.GenerateContentConfig(
                    system_instruction="You are a helpful e-commerce shopping and order tracking assistant. Use the search_products tool automatically when users ask about products, and use the user-specific order tools (get_my_orders, get_latest_order, get_order_status) securely when users ask about their personal order history or status.",
                    tools=tools,
                    temperature=0.7
                )
            )
            
            response = chat.send_message(prompt)
            return response.text
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Failed to fetch response from AI: {str(e)}")