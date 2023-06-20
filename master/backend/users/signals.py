from django.db.models.signals import post_save
from django.dispatch import receiver
from base.utils import preprocessing
from base.models import CombinedText,Preference
from django.contrib.auth.models import User

@receiver(post_save, sender=Preference)
def combine_texts_on_preference_save(sender, instance, **kwargs):
    print("Signal received! Texts will be combined.")
    combine_texts()

def combine_texts():

    users = User.objects.all()

    for user in users:
        user_preferences = Preference.objects.filter(user=user)
        texts = [preference.text for preference in user_preferences]
        cleaned_texts = [preprocessing(text) for text in texts]
        combined_text = ' '.join(cleaned_texts)
        combined_text_obj = CombinedText(user=user, combined_text=combined_text)
        combined_text_obj.save()
