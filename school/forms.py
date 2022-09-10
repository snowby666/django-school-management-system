from django import forms
from . import models
from django.core.validators import RegexValidator

CLASS_CHOICES = [
    ('KC', 'Không Chuyên'),
    ('CT', 'Chuyên Toán'),
    ('CV', 'Chuyên Văn'),
    ('CL', 'Chuyên Lý'),
    ('CH', 'Chuyên Hóa'),
    ('CS', 'Chuyên Sinh'),
    ('CTin', 'Chuyên Tin'),
    ('CA', 'Chuyên Anh')
]

phone_validator = RegexValidator(
    r"((^(\+84|84|0|0084){1})(3|5|7|8|9))+([0-9]{8})$", "Số điện thoại phải có định dạng (xxx)xxxxxxxxx hoặc 0xxxxxxxxx!")

class FormContact(forms.ModelForm):
    name = forms.CharField(max_length=150, label='Name', widget=forms.TextInput(attrs={
                           'placeholder': '...', 'class': 'form-control fh5co_contact_text_box'}))
    phone_number = forms.CharField(max_length=20, label='Phone', validators=[phone_validator], widget=forms.TextInput(
        attrs={'placeholder': '...',
               'class': 'form-control fh5co_contact_text_box',
               'pattern': '((^(\+84|84|0|0084){1})(3|5|7|8|9))+([0-9]{8})$',
               'title': 'Số điện thoại phải có định dạng (xxx)xxxxxxxxx hoặc 0xxxxxxxxx'}))
    email = forms.EmailField(label='...', widget=forms.TextInput(
        attrs={'placeholder': '...', 'class': 'form-control fh5co_contact_text_box'}))
    subject = forms.CharField(label='Subject', widget=forms.TextInput(
        attrs={'placeholder': '...', 'class': 'form-control fh5co_contact_text_box'}))
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': '...', 'class': 'form-control fh5co_contacts_message'}))

    class Meta:
        model = models.Contact
        fields = '__all__'

class FormAdmission(forms.ModelForm):
    name = forms.CharField(max_length=150, label='Name', widget=forms.TextInput(attrs={
                           'placeholder': 'Họ và Tên', 'class': 'form-control fh5co_contact_text_box'}))
    phone_number = forms.CharField(max_length=20, label='Phone', validators=[phone_validator], widget=forms.TextInput(
        attrs={'placeholder': 'Số điện thoại',
               'class': 'form-control fh5co_contact_text_box',
               'pattern': '((^(\+84|84|0|0084){1})(3|5|7|8|9))+([0-9]{8})$',
               'title': 'Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'class': 'form-control fh5co_contact_text_box'}))
    school = forms.CharField(label='School', widget=forms.TextInput(
        attrs={'placeholder': 'Trường', 'class': 'form-control fh5co_contact_text_box'}))
    classroom = forms.CharField(label='Classroom',widget=forms.Select(choices=CLASS_CHOICES, attrs={'placeholder': 'Lớp', 'class': 'form-control fh5co_contact_text_box'})
    )

    class Meta:
        model = models.Admission
        fields = '__all__'
        
        
class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=150, label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Mật khẩu', 'pattern': '(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
               'title': 'Tối thiểu 8 ký tự, ít nhất 1 chữ cái và 1 số', 'class': 'form-control fh5co_contact_text_box'}))
    confirm = forms.CharField(max_length=150, label='Confirm', widget=forms.PasswordInput(attrs={'placeholder': 'Xác nhận mật khẩu', 'class': 'form-control fh5co_contact_text_box'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control fh5co_contact_text_box'}))
    username = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Tên đăng nhập', 'pattern': '^[A-Za-z][A-Za-z0-9_]{6,12}$', 'title': 'Tối thiểu 6 ký tự, tối đa 12 ký tự và không sử dụng ký tự đặc biệt', 'class': 'form-control fh5co_contact_text_box'}))
    
    class Meta():
        model = models.User
        fields = ('username', 'email', 'password')
        
class UserProfileInfoForm(forms.ModelForm):
    fullname = forms.CharField(
        max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Họ và tên', 'class': 'form-control fh5co_contact_text_box'}))
    address = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Địa chỉ', 'class': 'form-control fh5co_contact_text_box'}))
    phone = forms.CharField(max_length=20, label = 'Phone', widget=forms.TextInput(
        attrs={'placeholder': 'Số điện thoại', 'pattern': '((^(\+84|84|0|0084){1})(3|5|7|8|9))+([0-9]{8})$',
               'title': 'Số điện thoại phải có định dạng (xxx)xxxxxxxxx hoặc 0xxxxxxxxx', 'class': 'form-control fh5co_contact_text_box'}))
    image = forms.ImageField(required=False)
    
    class Meta():
        model = models.UserProfileInfo
        exclude = ('user', )
        
        
class UpdateUserForm(forms.ModelForm):
    password = forms.CharField(max_length=150, label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Mật khẩu', 'pattern': '(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
               'title': 'Tối thiểu 8 ký tự, ít nhất 1 chữ cái và 1 số', 'class': 'form-control fh5co_contact_text_box'}))
    confirm = forms.CharField(max_length=150, label='Confirm', widget=forms.PasswordInput(attrs={'placeholder': 'Xác nhận mật khẩu', 'class': 'form-control fh5co_contact_text_box'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control fh5co_contact_text_box'}))

    class Meta():
        model = models.User
        fields = ('password', 'email')


class UpdateUserProfileInfoForm(forms.ModelForm):
    fullname = forms.CharField(
        max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Họ và tên', 'class': 'form-control fh5co_contact_text_box'}))
    address = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Địa chỉ', 'class': 'form-control fh5co_contact_text_box'}))
    phone = forms.CharField(max_length=20, label = 'Phone', widget=forms.TextInput(
        attrs={'placeholder': 'Số điện thoại', 'pattern': '((^(\+84|84|0|0084){1})(3|5|7|8|9))+([0-9]{8})$',
               'title': 'Số điện thoại phải có định dạng (xxx)xxxxxxxxx hoặc 0xxxxxxxxx', 'class': 'form-control fh5co_contact_text_box'}))
    image = forms.ImageField(required=False)

    class Meta():
        model = models.UserProfileInfo
        exclude = ('user', )
        
        
class CommentForm(forms.ModelForm):
    name = forms.CharField(required=False, max_length=150, widget=forms.TextInput(attrs={
                           'placeholder': 'Họ tên', 'class': 'form-control fh5co_contact_text_box'}))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'class': 'form-control fh5co_contact_text_box'}))
    content = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs={'placeholder': '...', 'class': 'form-control fh5co_contacts_message'}))
    class Meta:
        model = models.Comment
        fields = ('name', 'email', 'content')
        
    
    