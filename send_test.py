from app.notifier import send_whatsapp

def run_test():
    fake_alerts = [
        {
            "store": "Amazon",
            "price_usd": 74.99,
            "price_clp": 71240,
            "triggered_by": "USD",
            "link": "https://www.amazon.com/dp/B0BHJDY5NV"
        },
        {
            "store": "Falabella",
            "price_usd": 81.00,
            "price_clp": 72990,
            "triggered_by": "CLP",
            "link": "https://www.falabella.com/falabella-cl/product/12345/SSD"
        }
    ]
    
    product_name = "Samsung SSD 990 PRO 1TB Heatsink"
    
    print(f"Enviando mensaje de prueba para {product_name}...")
    success = send_whatsapp(fake_alerts, product_name, is_test=True)
    
    if success:
        print("✅ Test message sent successfully!")
    else:
        print("❌ Failed to send message. Check your .env variables.")

if __name__ == "__main__":
    run_test()
