from django.contrib import admin
from django import forms
from django.contrib import messages
from datetime import date
from .models import Cliente, Contrato, Tarifa, Medidor, Lectura, Boleta, Pago, NotificacionLectura, NotificacionPago, Usuario

# ==========================================================
# FORMS PERSONALIZADOS PARA MENÚS DESPLEGABLES
# ==========================================================

class ClienteAdminForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ MENÚ DESPLEGABLE para usuario_asociado
        usuarios = Usuario.objects.all()
        choices = [('', '---------')]  # Opción vacía
        choices += [(usuario.username, f"{usuario.username} ({usuario.rol})") for usuario in usuarios]
        self.fields['usuario_asociado'].widget = forms.Select(choices=choices)

class ContratoAdminForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ MENÚ DESPLEGABLE para cliente_numero
        clientes = Cliente.objects.all()
        choices = [('', '---------')]
        choices += [(cliente.numero_cliente, f"{cliente.numero_cliente} - {cliente.nombre}") for cliente in clientes]
        self.fields['cliente_numero'].widget = forms.Select(choices=choices)

class MedidorAdminForm(forms.ModelForm):
    class Meta:
        model = Medidor
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ MENÚ DESPLEGABLE para contrato_numero
        contratos = Contrato.objects.all()
        choices = [('', '---------')]
        choices += [(contrato.numero_contrato, f"{contrato.numero_contrato} - {contrato.estado}") for contrato in contratos]
        self.fields['contrato_numero'].widget = forms.Select(choices=choices)

class LecturaAdminForm(forms.ModelForm):
    class Meta:
        model = Lectura
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ MENÚ DESPLEGABLE para medidor_numero
        medidores = Medidor.objects.all()
        choices = [('', '---------')]
        choices += [(medidor.numero_medidor, f"{medidor.numero_medidor} - {medidor.ubicacion}") for medidor in medidores]
        self.fields['medidor_numero'].widget = forms.Select(choices=choices)

class BoletaAdminForm(forms.ModelForm):
    class Meta:
        model = Boleta
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ MENÚ DESPLEGABLE para cliente_numero
        clientes = Cliente.objects.all()
        choices = [('', '---------')]
        choices += [(cliente.numero_cliente, f"{cliente.numero_cliente} - {cliente.nombre}") for cliente in clientes]
        self.fields['cliente_numero'].widget = forms.Select(choices=choices)
        
        # ✅ MENÚ DESPLEGABLE para lectura_id
        lecturas = Lectura.objects.all()
        lectura_choices = [('', '---------')]
        lectura_choices += [(str(lectura.id), f"Lectura #{lectura.id} - {lectura.fecha_lectura}") for lectura in lecturas]
        self.fields['lectura_id'].widget = forms.Select(choices=lectura_choices)

class PagoAdminForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ✅ MENÚ DESPLEGABLE para boleta_id
        boletas = Boleta.objects.all()
        choices = [('', '---------')]
        choices += [(str(boleta.id), f"Boleta #{boleta.id} - ${boleta.monto_total}") for boleta in boletas]
        self.fields['boleta_id'].widget = forms.Select(choices=choices)

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - CLIENTE (MODIFICADO)
# ==========================================================
class ClienteAdmin(admin.ModelAdmin):
    form = ClienteAdminForm  # ✅ FORM PERSONALIZADO
    list_display = ('numero_cliente', 'nombre', 'email', 'telefono', 'usuario_asociado')
    list_filter = ('numero_cliente', 'usuario_asociado')
    search_fields = ('numero_cliente', 'nombre', 'email', 'telefono', 'usuario_asociado')
    ordering = ('numero_cliente',)
    
    fieldsets = (
        ('Información del Cliente', {'fields': ('numero_cliente', 'nombre')}),
        ('Contacto', {'fields': ('email', 'telefono')}),
        ('Relaciones', {'fields': ('usuario_asociado',)}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('numero_cliente',)
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - CONTRATO (MODIFICADO)
# ==========================================================
class ContratoAdmin(admin.ModelAdmin):
    form = ContratoAdminForm  # ✅ FORM PERSONALIZADO
    list_display = ('numero_contrato', 'cliente_numero', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'fecha_inicio', 'cliente_numero')
    search_fields = ('numero_contrato', 'cliente_numero')
    ordering = ('-fecha_inicio',)
    
    fieldsets = (
        ('Información del Contrato', {'fields': ('numero_contrato', 'estado')}),
        ('Relaciones', {'fields': ('cliente_numero',)}),
        ('Periodo de Vigencia', {'fields': ('fecha_inicio', 'fecha_fin')}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('numero_contrato',)
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - TARIFA
# ==========================================================
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('fecha_vigencia', 'precio', 'tipo_tarifa', 'tipo_cliente')
    list_filter = ('tipo_tarifa', 'tipo_cliente')
    search_fields = ('tipo_tarifa', 'tipo_cliente')
    ordering = ('-fecha_vigencia',)
    
    fieldsets = (
        ('Tipo de Tarifa', {'fields': ('tipo_tarifa', 'tipo_cliente')}),
        ('Valor y Vigencia', {'fields': ('precio', 'fecha_vigencia')}),
    )

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - MEDIDOR (MODIFICADO)
# ==========================================================
class MedidorAdmin(admin.ModelAdmin):
    form = MedidorAdminForm  # ✅ FORM PERSONALIZADO
    list_display = ('numero_medidor', 'contrato_numero', 'ubicacion', 'estado_medidor', 'fecha_instalacion')
    list_filter = ('estado_medidor', 'fecha_instalacion', 'contrato_numero')
    search_fields = ('numero_medidor', 'ubicacion', 'contrato_numero')
    ordering = ('numero_medidor',)
    
    fieldsets = (
        ('Identificación del Medidor', {'fields': ('numero_medidor', 'ubicacion')}),
        ('Relaciones', {'fields': ('contrato_numero',)}),
        ('Estado y Fecha', {'fields': ('estado_medidor', 'fecha_instalacion')}),
        ('Imágenes', {'fields': ('imagen_ubicacion', 'imagen_fisica')}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('numero_medidor', 'fecha_instalacion')
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - LECTURA (MODIFICADO)
# ==========================================================
class LecturaAdmin(admin.ModelAdmin):
    form = LecturaAdminForm  # ✅ FORM PERSONALIZADO
    list_display = ('fecha_lectura', 'medidor_numero', 'consumo_energetico', 'tipo_lectura', 'lectura_actual')
    list_filter = ('tipo_lectura', 'fecha_lectura', 'medidor_numero')
    search_fields = ('tipo_lectura', 'medidor_numero')
    ordering = ('-fecha_lectura',)
    
    fieldsets = (
        ('Datos de Lectura', {'fields': ('fecha_lectura', 'lectura_actual', 'tipo_lectura')}),
        ('Relaciones', {'fields': ('medidor_numero',)}),
        ('Consumo', {'fields': ('consumo_energetico',)}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('fecha_lectura',)
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - BOLETA (MODIFICADO)
# ==========================================================
class BoletaAdmin(admin.ModelAdmin):
    form = BoletaAdminForm  # ✅ FORM PERSONALIZADO
    list_display = ('fecha_emision', 'cliente_numero', 'fecha_vencimiento', 'monto_total', 'estado')
    list_filter = ('estado', 'fecha_emision', 'cliente_numero')
    search_fields = ('estado', 'consumo_energetico', 'cliente_numero')
    ordering = ('-fecha_emision',)
    
    fieldsets = (
        ('Información de la Boleta', {'fields': ('fecha_emision', 'monto_total', 'consumo_energetico')}),
        ('Relaciones', {'fields': ('cliente_numero', 'lectura_id')}),
        ('Estado y Vencimiento', {'fields': ('estado', 'fecha_vencimiento')}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('fecha_emision',)
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - PAGO (MODIFICADO)
# ==========================================================
class PagoAdmin(admin.ModelAdmin):
    form = PagoAdminForm  # ✅ FORM PERSONALIZADO
    list_display = ('fecha_pago', 'boleta_id', 'monto_pagado', 'metodo_pago', 'numero_referencia')
    list_filter = ('metodo_pago', 'estado_pago', 'boleta_id')
    search_fields = ('numero_referencia', 'metodo_pago', 'boleta_id')
    ordering = ('-fecha_pago',)
    
    fieldsets = (
        ('Información del Pago', {'fields': ('fecha_pago', 'monto_pagado', 'metodo_pago')}),
        ('Relaciones', {'fields': ('boleta_id',)}),
        ('Referencia y Estado', {'fields': ('numero_referencia', 'estado_pago')}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('fecha_pago', 'numero_referencia')
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - USUARIO
# ==========================================================
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'telefono')
    list_filter = ('rol',)
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    fieldsets = (
        ('Credenciales', {'fields': ('username', 'password')}),
        ('Información del usuario', {'fields': ('email', 'telefono', 'rol')}),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username',)
        return ()

# ==========================================================
# CONFIGURACIÓN DEL ADMIN - NOTIFICACIONES
# ==========================================================
class NotificacionLecturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'registro_consumo')
    search_fields = ('registro_consumo',)
    ordering = ('id',)
    
    fieldsets = (
        ('Información de Notificación', {'fields': ('registro_consumo',)}),
    )

class NotificacionPagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'deuda_pendiente')
    search_fields = ('deuda_pendiente',)
    ordering = ('id',)
    
    fieldsets = (
        ('Información de Notificación', {'fields': ('deuda_pendiente',)}),
    )

# ==========================================================
# REGISTRO DE MODELOS EN EL ADMIN
# ==========================================================
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Tarifa, TarifaAdmin)
admin.site.register(Medidor, MedidorAdmin)
admin.site.register(Lectura, LecturaAdmin)
admin.site.register(Boleta, BoletaAdmin)
admin.site.register(Pago, PagoAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(NotificacionLectura, NotificacionLecturaAdmin)
admin.site.register(NotificacionPago, NotificacionPagoAdmin)