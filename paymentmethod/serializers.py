from rest_framework.serializers import ModelSerializer
from .models import PaymentMethod

class PaymentMethodSerializer(ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'details', 'is_active', 'display']
    
    def validate_details(self, value):
        payment_method_name = self.initial_data.get('name')

        if payment_method_name == 'btc':  # Validation for Bitcoin
            if not value.get('wallet_address'):
                raise serializers.ValidationError("Bitcoin requires a wallet address.")
        elif payment_method_name == 'paypal':  # Validation for PayPal
            if not value.get('email'):
                raise serializers.ValidationError("PayPal requires an email.")
        elif payment_method_name == 'cashapp':  # Validation for CashApp
            if not value.get('cashtag'):
                raise serializers.ValidationError("CashApp requires a cashtag.")
        elif payment_method_name == 'bank':  # Validation for Bank
            required_fields = ['account_number', 'bank_name', 'account_name']
            for field in required_fields:
                if not value.get(field):
                    raise serializers.ValidationError(f"Bank requires {field}.")
        elif payment_method_name == 'zelle':  # Validation for Zelle
            if not (value.get('email') or value.get('phone_number')):
                raise serializers.ValidationError("Zelle requires an email or phone number.")
        return value
