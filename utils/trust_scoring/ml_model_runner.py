from django.conf import settings


def get_prob_trust_score(features_df):
	return list(settings.SCORING_ML_MODEL.predict_proba(features_df))[0][1] * 100
