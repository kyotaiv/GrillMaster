from django import forms
from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth.models import User
from grillmaster.models import Genero, Productos, Contacto, OpcionesContacto, Registro_cliente

class SignUpForm(UserCreationForm):
    genero=forms.ModelChoiceField(Genero.objects.all(),required=True,label="Genero")
    fecha_nac= forms.DateField()
    class Meta:
        model=User
        fields = ['username', 'password1', 'password2', 'email', 'genero', 'fecha_nac']
    pass

class ContactForm(forms.ModelForm):
    REASON_CHOICES = [
        ("cotizacion", "Cotización"),
        ("problema", "Problema Con Servicio"),
    ]
    reason = forms.ModelChoiceField(OpcionesContacto.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control',
            'id': 'reason',
        }
    ))
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={
                'id': 'image',
                'class': 'form-control-file',
            }
        )
    )
    class Meta:
        model = Contacto
        fields = ('name', 'email', 'description', 'reason', 'image')
        labels = {
            'name': 'Nombre real',
            'email': 'Correo',
            'description': 'Descripcion',
            'reason': 'Razon de contacto',
            'image': 'Archivo adjunto',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre...',
                    'id': 'name',
                    'class': 'form-control',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Ingrese correo...',
                    'id': 'email',
                    'class': 'form-control',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese descripcion...',
                    'id': 'description',
                    'class': 'form-control',
                    'rows': '4',
                    'cols': '50',
                }
            ),
        }
    pass

class ProductosForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ['id','name', 'description', 'price', 'stock', 'categoria', 'image']
        labels ={
            'id' : 'ID',
            'name' : 'Nombre',
            'description': 'Descripción',
            'price': 'Precio',
            'stock': 'Stock',
            'categoria':'Categoria',
            'image': 'Imagen',
        }
        widgets = {
            'id': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese id...',
                    'id': 'id',
                    'class': 'form-control',
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre...',
                    'id': 'name',
                    'class': 'form-control',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese descripción...',
                    'id': 'description',
                    'class': 'form-control',
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'placeholder': 'Ingrese precio...',
                    'id': 'price',
                    'class': 'form-control',
                }
            ),
            'stock': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'id': 'stock',
                }
            ),
            'categoria': forms.Select(
                attrs={
                    'id':'categoria',
                    'class':'form-control',
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'id': 'image',
                }
            )
        }

class UserProfileForm(forms.ModelForm):
    genero = forms.ModelChoiceField(Genero.objects.all(), required=True, label="Género")
    fecha_nac = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'text', 
            'placeholder': 'Ejemplo: 1985-10-10',
            'pattern': '[0-9]{4}-[0-9]{2}-[0-9]{2}',
            'title': 'Se ingresa como AÑO-MES-DIA'
        }),
        input_formats=['%Y-%m-%d']
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'off'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'genero', 'fecha_nac']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'registro_cliente'):
            self.fields['fecha_nac'].initial = self.instance.registro_cliente.fecha_nac
            self.fields['genero'].initial = self.instance.registro_cliente.id_genero

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            registro_cliente, created = Registro_cliente.objects.get_or_create(user=user)
            registro_cliente.fecha_nac = self.cleaned_data['fecha_nac']
            registro_cliente.id_genero = self.cleaned_data['genero']
            registro_cliente.save()
        return user
