from django.contrib import admin
from .models import Identified, Profile, MoneyOut, Transaction
from django.utils.html import format_html

import time
from . import serialazers

class IdentifiedAdmin(admin.ModelAdmin):
    list_display = ('fullname','is_identified')
    readonly_fields = ('display_iD_image','display_address_image', 'display_selfie_image')
    exclude = ('user_id','id_image', 'address_image', 'selfie_image')

    def display_iD_image(self, obj):
        return format_html('<img src="data:image/jpeg;base64,{}" width="400" height="600" />',
                           obj.id_image)
    display_iD_image.short_description = 'ID Image'

    def display_address_image(self, obj):
        return format_html('<img src="data:image/jpeg;base64,{}" width="400" height="600" />',
                           obj.address_image)
    display_address_image.short_description = 'Address Image'

    def display_selfie_image(self, obj):
        return format_html('<img src="data:image/jpeg;base64,{}" width="400" height="600" />',
                           obj.selfie_image)
    display_selfie_image.short_description = 'Selfie Image'


    def save_model(self, request, obj, form, change):
        # Ma'lumot o'zgartirilganda ishlatiladigan funksiya
        if 'is_identified' in form.changed_data and form.cleaned_data['is_identified'] == True:
            a = form.cleaned_data['user_id']
            profile = Profile.objects.get(id=a)
            link = profile.friend_referal_link
            profile.is_identified = True
            if link != None:
                profile.balance_usdt += 0.1
                profile.balance_netbo += 0.2
                pr_username = str(profile.id)
                profile.save()
                taim = int(time.time())
                data = {"profile_id":pr_username, "balance_usdt":0.1,'balance_netbo':0.2,"created_at":taim}
                tran = serialazers.Tranzaktionserialazer(data=data)
                if tran.is_valid():
                    tran.save()

                frend = Profile.objects.get(referal_link=link)
                frend.number_people += 1
                frend.balance_usdt += 0.05
                frend.balance_netbo += 0.1
                fr_username = str(frend.id)
                data = {"profile_id":fr_username, "balance_usdt":0.05,'balance_netbo':0.1,"created_at":taim}
                frend.save()
                tran = serialazers.Tranzaktionserialazer(data=data)
                if tran.is_valid():
                    tran.save()
        else:
            a = form.cleaned_data['user_id']
            profile = Profile.objects.get(id=a)
            profile.is_identified = False
            profile.save()

        # super() metodini chaqirishni unutmang
        super().save_model(request, obj, form, change)

class ModelOutAdmin(admin.ModelAdmin):
    list_display = ('profile_id','is_identified')
    list_filter = (('is_identified', admin.BooleanFieldListFilter), )

    def save_model(self, request, obj, form, change):
        # Ma'lumot o'zgartirilganda ishlatiladigan funksiya
        if 'is_identified' in form.changed_data and form.cleaned_data['is_identified'] == False:
            a = form.cleaned_data['profile_id']
            profile = Profile.objects.get(id=a)
            b = form.cleaned_data['balance_netbo']
            profile.balance_netbo += b
            profile.save()


        # super() metodini chaqirishni unutmang
        super().save_model(request, obj, form, change)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_identified')
    exclude = ('profile_image',)
    search_fields = ('username','email')

admin.site.register(Identified, IdentifiedAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(MoneyOut, ModelOutAdmin)
admin.site.register(Transaction)