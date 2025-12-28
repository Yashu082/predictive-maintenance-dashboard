from rest_framework import serializers


class SensorDataSerializer(serializers.Serializer):
    """Serializer for sensor input data - flexible for different datasets"""
    # For synthetic dataset
    temperature = serializers.FloatField(required=False)
    vibration = serializers.FloatField(required=False)
    pressure = serializers.FloatField(required=False)
    
    # For NASA dataset (Hugging Face format) - operational settings
    setting_1 = serializers.FloatField(required=False)
    setting_2 = serializers.FloatField(required=False)
    setting_3 = serializers.FloatField(required=False)
    
    # For NASA dataset (Hugging Face format) - key sensors with underscore
    s_2 = serializers.FloatField(required=False)
    s_3 = serializers.FloatField(required=False)
    s_4 = serializers.FloatField(required=False)
    s_7 = serializers.FloatField(required=False)
    s_8 = serializers.FloatField(required=False)
    s_9 = serializers.FloatField(required=False)
    s_11 = serializers.FloatField(required=False)
    s_12 = serializers.FloatField(required=False)
    s_13 = serializers.FloatField(required=False)
    s_14 = serializers.FloatField(required=False)
    s_15 = serializers.FloatField(required=False)
    s_17 = serializers.FloatField(required=False)
    s_20 = serializers.FloatField(required=False)
    s_21 = serializers.FloatField(required=False)
    
    # Rolling statistics (optional, will be calculated if missing)
    s_2_mean = serializers.FloatField(required=False)
    s_2_std = serializers.FloatField(required=False)
    s_3_mean = serializers.FloatField(required=False)
    s_3_std = serializers.FloatField(required=False)
    s_4_mean = serializers.FloatField(required=False)
    s_4_std = serializers.FloatField(required=False)
    s_7_mean = serializers.FloatField(required=False)
    s_7_std = serializers.FloatField(required=False)
    s_8_mean = serializers.FloatField(required=False)
    s_8_std = serializers.FloatField(required=False)
    
    def validate(self, data):
        """Ensure at least some sensor data is provided"""
        # Check for synthetic dataset fields
        synthetic_fields = ['temperature', 'vibration', 'pressure']
        # Check for NASA Hugging Face format
        nasa_fields = ['setting_1', 'setting_2', 'setting_3', 's_2', 's_3', 's_4', 's_7', 's_8', 's_9', 
                       's_11', 's_12', 's_13', 's_14', 's_15', 's_17', 's_20', 's_21']
        
        has_synthetic = any(data.get(field) is not None for field in synthetic_fields)
        has_nasa = any(data.get(field) is not None for field in nasa_fields)
        
        if not (has_synthetic or has_nasa):
            raise serializers.ValidationError(
                "At least one sensor value must be provided. "
                "For synthetic dataset: temperature, vibration, pressure. "
                "For NASA dataset: setting_1-setting_3 and sensors s_2, s_3, etc."
            )
        return data


class PredictionResponseSerializer(serializers.Serializer):
    """Serializer for prediction response"""
    failure_probability = serializers.FloatField()
    risk_level = serializers.CharField()
    prediction = serializers.IntegerField()
