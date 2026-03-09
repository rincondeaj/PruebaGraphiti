from interfaces import PaymentGateway

class PaymentFactory:
    @staticmethod
    def get_payment_gateway(provider_name: str) -> PaymentGateway:

        from main import StripeAdapter, PayPalAdapter 
        
        match provider_name.lower():
            case "stripe":
                return StripeAdapter()
            case "paypal":
                return PayPalAdapter()
            case _:
                raise ValueError(f"Unknown provider: {provider_name}")