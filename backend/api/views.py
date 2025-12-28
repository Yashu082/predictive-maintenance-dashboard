"""
API Views for Predictive Maintenance
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import SensorDataSerializer, PredictionResponseSerializer
from .ml_service import MLService


@api_view(['POST'])
def predict(request):
    """
    Predict equipment failure probability from sensor data
    
    Supports both synthetic and NASA datasets:
    
    Synthetic dataset JSON:
    {
        "temperature": 95.5,
        "vibration": 6.2,
        "pressure": 132.0
    }
    
    NASA dataset JSON:
    {
        "op1": 0.0,
        "op2": 0.0,
        "op3": 100.0,
        "s2": 518.67,
        "s3": 1583.0,
        ...
    }
    
    Returns:
    {
        "failure_probability": 0.85,
        "risk_level": "High",
        "prediction": 1
    }
    """
    # Validate input
    serializer = SensorDataSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'error': 'Invalid input data', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Extract validated data (remove None values)
    sensor_data = {k: v for k, v in serializer.validated_data.items() if v is not None}
    
    try:
        # Get prediction from ML service
        result = MLService.predict(**sensor_data)
        
        # Validate and return response
        response_serializer = PredictionResponseSerializer(data=result)
        if response_serializer.is_valid():
            return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Prediction failed', 'details': response_serializer.errors},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    except FileNotFoundError as e:
        return Response(
            {'error': 'Model not found', 'details': str(e)},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except ValueError as e:
        return Response(
            {'error': 'Invalid input', 'details': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': 'Prediction failed', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_features(request):
    """
    Get the list of required features for the current model
    """
    try:
        features = MLService.get_required_features()
        return Response({'features': features}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Failed to get features', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
