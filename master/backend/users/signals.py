from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from base.utils import preprocessing
from base.models import CombinedText,Preference

@receiver(post_save, sender=Preference)
@receiver(post_delete, sender=Preference)
def combine_texts_on_preference_change(sender, instance, **kwargs):
    combine_texts()

def combine_texts():
    from django.contrib.auth.models import User
    
    users = User.objects.all()

    for user in users:
        user_preferences = Preference.objects.filter(user=user)
        texts = [preference.text for preference in user_preferences]
        cleaned_texts = [preprocessing(text) for text in texts]
        combined_text = ' '.join(cleaned_texts)

        # Update or create CombinedText object for the user
        combined_text_obj, _ = CombinedText.objects.update_or_create(
            user=user,
            defaults={'combined_text': combined_text}
        )
