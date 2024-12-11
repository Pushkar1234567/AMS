from rest_framework import serializers 
from app.models import User, Roster, Shift, Attendance
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password,check_password
import re

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print("------Inside the function--------")
        print(attrs)

        user = User.objects.filter(username = attrs.get('username')).first()
        if not user:
            raise serializers.ValidationError("User not found")
        if user.is_active == False:
            raise serializers.ValidationError("User not active")
        
        # if not check_password(attrs.get('password'), user.password):
        if user.password != attrs.get('password'):
            raise serializers.ValidationError("Wrong Password")
        
        refresh = self.get_token(user)
        print("Your token is :  ",refresh)
        data = {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        }
        return data
        # Use 'username' as the login field
        # try:
            
        #     data['username'] = self.user.username  # Add username to the token response
        #     print("Here is the data ------",data)
        # except Exception as E:
        #     print("Error is -------",E)
        # return data

class RegisterSerializer(serializers.ModelSerializer):

    def create(self,validated_data):
        # print(**validated_data)
        password = validated_data.get('password')
        if len(password)<8:
            raise serializers.ValidationError("It should be greeter than 8 characters")
        elif not re.search(r"\d",password):
            raise serializers.ValidationError("It should contains digits")
        elif not re.search(r"[~!@#$%^&*()_+]",password):
            raise serializers.ValidationError("It should contain special character")
        hashed_password = make_password(validated_data.get('password'))
        # print(check_password(validated_data['password'], hashed_password))
        validated_data['password'] = hashed_password

        instance = super().create(validated_data)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    def update(self,instance, validated_data):
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.email = validated_data.get('email',instance.email)
        instance.role = validated_data.get('role',instance.role)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['id', 'first_name', 'email', 'role']


class RosterSerializer(serializers.ModelSerializer):

    def create(self,validated_data):
        print("inside the function")
        user = validated_data.get('user')
        try:
            print("user_id ",user.id)
        except Exception as E:
            print(E)
        if user.role != "Staff":
            raise serializers.ValidationError({"Error":"Shifts are only assigned to Staff users"})

        user = Roster.objects.create(**validated_data)

        try:
            working_days = validated_data.get('working_days')
            days = ", ".join(working_days.keys())
            shift_timings = ", ".join(working_days.values())
            roster_id = user.id
            staff_id = user.user_id
            print(f"data is {days} {shift_timings} {roster_id} {staff_id}")
            staff_user = Shift.objects.create(day = days, shift_time = shift_timings, roster_id = roster_id, staff_id = staff_id)
            staff_user.save()
        except Exception as E:
            print("Error -- ",E)
        
        return user


    class Meta:
        model = Roster
        fields = ['id', 'user', 'working_days', 'weekly_offs']

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ['id', 'roster', 'day', 'shift_time', 'staff']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'staff', 'timestamp', 'shift']

# class StaffCreationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'email']

#     def create(self, validated_data):
#         # Create a Staff account
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password'],
#             email=validated_data.get('email'),
#             role='Staff'
#         )
#         return user
