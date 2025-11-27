from rest_framework import serializers
from personal.models import Personal


class PersonalSerializer(serializers.ModelSerializer):
    """Serializer para lectura y actualización de Personal"""
    
    rol_display = serializers.CharField(source='get_rol_display', read_only=True)
    nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = Personal
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'nombre_completo',
            'rol',
            'rol_display',
            'turno',
            'numero_empleado',
            'telefono',
            'is_active',
            'date_joined',
            'last_login',
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
    
    def get_nombre_completo(self, obj):
        return obj.get_full_name() or obj.username


class PersonalCreateSerializer(serializers.ModelSerializer):
    """Serializer para creación de Personal con contraseña"""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = Personal
        fields = [
            'id',
            'username',
            'email',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'rol',
            'turno',
            'numero_empleado',
            'telefono',
        ]
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Las contraseñas no coinciden'
            })
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = Personal(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class PersonalMinimalSerializer(serializers.ModelSerializer):
    """Serializer mínimo para referencias en otras entidades"""
    
    nombre_completo = serializers.SerializerMethodField()
    
    class Meta:
        model = Personal
        fields = ['id', 'username', 'nombre_completo', 'rol']
    
    def get_nombre_completo(self, obj):
        return obj.get_full_name() or obj.username
