from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import geopy.distance

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
import datetime

class Crew(models.Model):
	position_choices = [
		('captain', 'Captain'),
		('chief_mate', 'Chief Mate'),
		('second_mate', 'Second Mate'),
		('third_mate', 'Third Mate'),
		('deck_cadet', 'Deck Cadet'),
		('chief_engineer', 'Chief Engineer'),
		('second_engineer', 'Second Engineer'),
		('third_engineer', 'Third Engineer'),
		('fourth_engineer', 'Fourth Engineer'),
		('engine_cadet', 'Engine Cadet'),
		('electrician', 'Electrician'),
		('boatswain', 'Boatswain'),
		('pump_man', 'Pump Man'),
		('able_bodied_seaman', 'Able Bodied Seaman'),
		('ordinary_seaman', 'Ordinary Seaman'),
		('fitter', 'Fitter'),
		('oiler', 'Oiler'),
		('wiper', 'Wiper'),
		('chief_cook', 'Chief Cook'),
		('steward', 'Steward'),
	]
	sex_choices = [
		('male', 'Male'),
		('female', 'Female'),
	]
	country_choices = [('Afghanistan', 'Afghanistan'),('Åland Islands', 'Åland Islands'),('Albania', 'Albania'),('Algeria', 'Algeria'),('American Samoa', 'American Samoa'),('Andorra', 'Andorra'),('Angola', 'Angola'),('Anguilla', 'Anguilla'),('Antarctica', 'Antarctica'),('Antigua & Barbuda', 'Antigua & Barbuda'),('Argentina', 'Argentina'),('Armenia', 'Armenia'),('Aruba', 'Aruba'),('Australia', 'Australia'),('Austria', 'Austria'),('Azerbaijan', 'Azerbaijan'),('Bahamas', 'Bahamas'),('Bahrain', 'Bahrain'),('Bangladesh', 'Bangladesh'),('Barbados', 'Barbados'),('Belarus', 'Belarus'),('Belgium', 'Belgium'),('Belize', 'Belize'),('Benin', 'Benin'),('Bermuda', 'Bermuda'),('Bhutan', 'Bhutan'),('Bolivia', 'Bolivia'),('Bosnia & Herzegovina', 'Bosnia & Herzegovina'),('Botswana', 'Botswana'),('Bouvet Island', 'Bouvet Island'),('Brazil', 'Brazil'),('British Indian Ocean Territory', 'British Indian Ocean Territory'),('British Virgin Islands', 'British Virgin Islands'),('Brunei', 'Brunei'),('Bulgaria', 'Bulgaria'),('Burkina Faso', 'Burkina Faso'),('Burundi', 'Burundi'),('Cambodia', 'Cambodia'),('Cameroon', 'Cameroon'),('Canada', 'Canada'),('Cape Verde', 'Cape Verde'),('Caribbean Netherlands', 'Caribbean Netherlands'),('Cayman Islands', 'Cayman Islands'),('Central African Republic', 'Central African Republic'),('Chad', 'Chad'),('Chile', 'Chile'),('China', 'China'),('Christmas Island', 'Christmas Island'),('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands'),('Colombia', 'Colombia'),('Comoros', 'Comoros'),('Congo - Brazzaville', 'Congo - Brazzaville'),('Congo - Kinshasa', 'Congo - Kinshasa'),('Cook Islands', 'Cook Islands'),('Costa Rica', 'Costa Rica'),('Côte d’Ivoire', 'Côte d’Ivoire'),('Croatia', 'Croatia'),('Cuba', 'Cuba'),('Curaçao', 'Curaçao'),('Cyprus', 'Cyprus'),('Czechia', 'Czechia'),('Denmark', 'Denmark'),('Djibouti', 'Djibouti'),('Dominica', 'Dominica'),('Dominican Republic', 'Dominican Republic'),('Ecuador', 'Ecuador'),('Egypt', 'Egypt'),('El Salvador', 'El Salvador'),('Equatorial Guinea', 'Equatorial Guinea'),('Eritrea', 'Eritrea'),('Estonia', 'Estonia'),('Eswatini', 'Eswatini'),('Ethiopia', 'Ethiopia'),('Falkland Islands', 'Falkland Islands'),('Faroe Islands', 'Faroe Islands'),('Fiji', 'Fiji'),('Finland', 'Finland'),('France', 'France'),('French Guiana', 'French Guiana'),('French Polynesia', 'French Polynesia'),('French Southern Territories', 'French Southern Territories'),('Gabon', 'Gabon'),('Gambia', 'Gambia'),('Georgia', 'Georgia'),('Germany', 'Germany'),('Ghana', 'Ghana'),('Gibraltar', 'Gibraltar'),('Greece', 'Greece'),('Greenland', 'Greenland'),('Grenada', 'Grenada'),('Guadeloupe', 'Guadeloupe'),('Guam', 'Guam'),('Guatemala', 'Guatemala'),('Guernsey', 'Guernsey'),('Guinea', 'Guinea'),('Guinea-Bissau', 'Guinea-Bissau'),('Guyana', 'Guyana'),('Haiti', 'Haiti'),('Heard & McDonald Islands', 'Heard & McDonald Islands'),('Honduras', 'Honduras'),('Hong Kong SAR China', 'Hong Kong SAR China'),('Hungary', 'Hungary'),('Iceland', 'Iceland'),('India', 'India'),('Indonesia', 'Indonesia'),('Iran', 'Iran'),('Iraq', 'Iraq'),('Ireland', 'Ireland'),('Isle of Man', 'Isle of Man'),('Israel', 'Israel'),('Italy', 'Italy'),('Jamaica', 'Jamaica'),('Japan', 'Japan'),('Jersey', 'Jersey'),('Jordan', 'Jordan'),('Kazakhstan', 'Kazakhstan'),('Kenya', 'Kenya'),('Kiribati', 'Kiribati'),('Kuwait', 'Kuwait'),('Kyrgyzstan', 'Kyrgyzstan'),('Laos', 'Laos'),('Latvia', 'Latvia'),('Lebanon', 'Lebanon'),('Lesotho', 'Lesotho'),('Liberia', 'Liberia'),('Libya', 'Libya'),('Liechtenstein', 'Liechtenstein'),('Lithuania', 'Lithuania'),('Luxembourg', 'Luxembourg'),('Macao SAR China', 'Macao SAR China'),('Madagascar', 'Madagascar'),('Malawi', 'Malawi'),('Malaysia', 'Malaysia'),('Maldives', 'Maldives'),('Mali', 'Mali'),('Malta', 'Malta'),('Marshall Islands', 'Marshall Islands'),('Martinique', 'Martinique'),('Mauritania', 'Mauritania'),('Mauritius', 'Mauritius'),('Mayotte', 'Mayotte'),('Mexico', 'Mexico'),('Micronesia', 'Micronesia'),('Moldova', 'Moldova'),('Monaco', 'Monaco'),('Mongolia', 'Mongolia'),('Montenegro', 'Montenegro'),('Montserrat', 'Montserrat'),('Morocco', 'Morocco'),('Mozambique', 'Mozambique'),('Myanmar (Burma)', 'Myanmar (Burma)'),('Namibia', 'Namibia'),('Nauru', 'Nauru'),('Nepal', 'Nepal'),('Netherlands', 'Netherlands'),('New Caledonia', 'New Caledonia'),('New Zealand', 'New Zealand'),('Nicaragua', 'Nicaragua'),('Niger', 'Niger'),('Nigeria', 'Nigeria'),('Niue', 'Niue'),('Norfolk Island', 'Norfolk Island'),('North Korea', 'North Korea'),('North Macedonia', 'North Macedonia'),('Northern Mariana Islands', 'Northern Mariana Islands'),('Norway', 'Norway'),('Oman', 'Oman'),('Pakistan', 'Pakistan'),('Palau', 'Palau'),('Palestinian Territories', 'Palestinian Territories'),('Panama', 'Panama'),('Papua New Guinea', 'Papua New Guinea'),('Paraguay', 'Paraguay'),('Peru', 'Peru'),('Philippines', 'Philippines'),('Pitcairn Islands', 'Pitcairn Islands'),('Poland', 'Poland'),('Portugal', 'Portugal'),('Puerto Rico', 'Puerto Rico'),('Qatar', 'Qatar'),('Réunion', 'Réunion'),('Romania', 'Romania'),('Russia', 'Russia'),('Rwanda', 'Rwanda'),('Samoa', 'Samoa'),('San Marino', 'San Marino'),('São Tomé & Príncipe', 'São Tomé & Príncipe'),('Saudi Arabia', 'Saudi Arabia'),('Senegal', 'Senegal'),('Serbia', 'Serbia'),('Seychelles', 'Seychelles'),('Sierra Leone', 'Sierra Leone'),('Singapore', 'Singapore'),('Sint Maarten', 'Sint Maarten'),('Slovakia', 'Slovakia'),('Slovenia', 'Slovenia'),('Solomon Islands', 'Solomon Islands'),('Somalia', 'Somalia'),('South Africa', 'South Africa'),('South Georgia & South Sandwich Islands', 'South Georgia & South Sandwich Islands'),('South Korea', 'South Korea'),('South Sudan', 'South Sudan'),('Spain', 'Spain'),('Sri Lanka', 'Sri Lanka'),('St. Barthélemy', 'St. Barthélemy'),('St. Helena', 'St. Helena'),('St. Kitts & Nevis', 'St. Kitts & Nevis'),('St. Lucia', 'St. Lucia'),('St. Martin', 'St. Martin'),('St. Pierre & Miquelon', 'St. Pierre & Miquelon'),('St. Vincent & Grenadines', 'St. Vincent & Grenadines'),('Sudan', 'Sudan'),('Suriname', 'Suriname'),('Svalbard & Jan Mayen', 'Svalbard & Jan Mayen'),('Sweden', 'Sweden'),('Switzerland', 'Switzerland'),('Syria', 'Syria'),('Taiwan', 'Taiwan'),('Tajikistan', 'Tajikistan'),('Tanzania', 'Tanzania'),('Thailand', 'Thailand'),('Timor-Leste', 'Timor-Leste'),('Togo', 'Togo'),('Tokelau', 'Tokelau'),('Tonga', 'Tonga'),('Trinidad & Tobago', 'Trinidad & Tobago'),('Tunisia', 'Tunisia'),('Turkey', 'Turkey'),('Turkmenistan', 'Turkmenistan'),('Turks & Caicos Islands', 'Turks & Caicos Islands'),('Tuvalu', 'Tuvalu'),('U.S. Outlying Islands', 'U.S. Outlying Islands'),('U.S. Virgin Islands', 'U.S. Virgin Islands'),('Uganda', 'Uganda'),('Ukraine', 'Ukraine'),('United Arab Emirates', 'United Arab Emirates'),('United Kingdom', 'United Kingdom'),('United States', 'United States'),('Uruguay', 'Uruguay'),('Uzbekistan', 'Uzbekistan'),('Vanuatu', 'Vanuatu'),('Vatican City', 'Vatican City'),('Venezuela', 'Venezuela'),('Vietnam', 'Vietnam'),('Wallis & Futuna', 'Wallis & Futuna'),('Western Sahara', 'Western Sahara'),('Yemen', 'Yemen'),('Zambia', 'Zambia'),('Zimbabwe', 'Zimbabwe')]

	first_name = models.CharField(max_length=254)
	last_name = models.CharField(max_length=254)
	middle_name = models.CharField(max_length=254)
	phone = models.CharField(max_length=254)
	email = models.EmailField(max_length=254)
	sex = models.CharField(max_length=254, choices=sex_choices)
	birth_date = models.DateField()
	address = models.CharField(max_length=2540)
	country_of_residence = models.CharField(max_length=254, choices=country_choices)
	position = models.CharField(max_length=254, choices=position_choices)
	employment_date = models.DateField(auto_now_add=True)
	termination_date = models.DateField(default=timezone.now()+datetime.timedelta(days=365*3))


class Ship(models.Model):
	speed_class_choices = [
		('normal', 'Normal (23 Knots)'),
		('slow_streaming', 'Slow Streaming (19 Knots)'),
		('extra_slow_streaming', 'Extra Slow Streaming (16.5 Knots)'),
		('minimal_costs', 'Minimal Costs (13.5 Knots)'),
	]
	vessel_type_choices = [
		('cargo_vessel', 'Cargo Vessel'),
		('tanker', 'Tanker'),
		('passenger_vessel', 'Passenger Vessel'),
		('high_speed_craft', 'High Speed Craft'),
		('tugs_and_special_craft', 'Tugs & Special Craft'),
		('fishing', 'Fishing'),
		('pleasure_craft', 'Pleasure Craft'),
	]
	status_choices = [
		('active', 'Active'),
		('not_active', 'Not Active'),
	]

	country_choices = [('Afghanistan', 'Afghanistan'),('Åland Islands', 'Åland Islands'),('Albania', 'Albania'),('Algeria', 'Algeria'),('American Samoa', 'American Samoa'),('Andorra', 'Andorra'),('Angola', 'Angola'),('Anguilla', 'Anguilla'),('Antarctica', 'Antarctica'),('Antigua & Barbuda', 'Antigua & Barbuda'),('Argentina', 'Argentina'),('Armenia', 'Armenia'),('Aruba', 'Aruba'),('Australia', 'Australia'),('Austria', 'Austria'),('Azerbaijan', 'Azerbaijan'),('Bahamas', 'Bahamas'),('Bahrain', 'Bahrain'),('Bangladesh', 'Bangladesh'),('Barbados', 'Barbados'),('Belarus', 'Belarus'),('Belgium', 'Belgium'),('Belize', 'Belize'),('Benin', 'Benin'),('Bermuda', 'Bermuda'),('Bhutan', 'Bhutan'),('Bolivia', 'Bolivia'),('Bosnia & Herzegovina', 'Bosnia & Herzegovina'),('Botswana', 'Botswana'),('Bouvet Island', 'Bouvet Island'),('Brazil', 'Brazil'),('British Indian Ocean Territory', 'British Indian Ocean Territory'),('British Virgin Islands', 'British Virgin Islands'),('Brunei', 'Brunei'),('Bulgaria', 'Bulgaria'),('Burkina Faso', 'Burkina Faso'),('Burundi', 'Burundi'),('Cambodia', 'Cambodia'),('Cameroon', 'Cameroon'),('Canada', 'Canada'),('Cape Verde', 'Cape Verde'),('Caribbean Netherlands', 'Caribbean Netherlands'),('Cayman Islands', 'Cayman Islands'),('Central African Republic', 'Central African Republic'),('Chad', 'Chad'),('Chile', 'Chile'),('China', 'China'),('Christmas Island', 'Christmas Island'),('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands'),('Colombia', 'Colombia'),('Comoros', 'Comoros'),('Congo - Brazzaville', 'Congo - Brazzaville'),('Congo - Kinshasa', 'Congo - Kinshasa'),('Cook Islands', 'Cook Islands'),('Costa Rica', 'Costa Rica'),('Côte d’Ivoire', 'Côte d’Ivoire'),('Croatia', 'Croatia'),('Cuba', 'Cuba'),('Curaçao', 'Curaçao'),('Cyprus', 'Cyprus'),('Czechia', 'Czechia'),('Denmark', 'Denmark'),('Djibouti', 'Djibouti'),('Dominica', 'Dominica'),('Dominican Republic', 'Dominican Republic'),('Ecuador', 'Ecuador'),('Egypt', 'Egypt'),('El Salvador', 'El Salvador'),('Equatorial Guinea', 'Equatorial Guinea'),('Eritrea', 'Eritrea'),('Estonia', 'Estonia'),('Eswatini', 'Eswatini'),('Ethiopia', 'Ethiopia'),('Falkland Islands', 'Falkland Islands'),('Faroe Islands', 'Faroe Islands'),('Fiji', 'Fiji'),('Finland', 'Finland'),('France', 'France'),('French Guiana', 'French Guiana'),('French Polynesia', 'French Polynesia'),('French Southern Territories', 'French Southern Territories'),('Gabon', 'Gabon'),('Gambia', 'Gambia'),('Georgia', 'Georgia'),('Germany', 'Germany'),('Ghana', 'Ghana'),('Gibraltar', 'Gibraltar'),('Greece', 'Greece'),('Greenland', 'Greenland'),('Grenada', 'Grenada'),('Guadeloupe', 'Guadeloupe'),('Guam', 'Guam'),('Guatemala', 'Guatemala'),('Guernsey', 'Guernsey'),('Guinea', 'Guinea'),('Guinea-Bissau', 'Guinea-Bissau'),('Guyana', 'Guyana'),('Haiti', 'Haiti'),('Heard & McDonald Islands', 'Heard & McDonald Islands'),('Honduras', 'Honduras'),('Hong Kong SAR China', 'Hong Kong SAR China'),('Hungary', 'Hungary'),('Iceland', 'Iceland'),('India', 'India'),('Indonesia', 'Indonesia'),('Iran', 'Iran'),('Iraq', 'Iraq'),('Ireland', 'Ireland'),('Isle of Man', 'Isle of Man'),('Israel', 'Israel'),('Italy', 'Italy'),('Jamaica', 'Jamaica'),('Japan', 'Japan'),('Jersey', 'Jersey'),('Jordan', 'Jordan'),('Kazakhstan', 'Kazakhstan'),('Kenya', 'Kenya'),('Kiribati', 'Kiribati'),('Kuwait', 'Kuwait'),('Kyrgyzstan', 'Kyrgyzstan'),('Laos', 'Laos'),('Latvia', 'Latvia'),('Lebanon', 'Lebanon'),('Lesotho', 'Lesotho'),('Liberia', 'Liberia'),('Libya', 'Libya'),('Liechtenstein', 'Liechtenstein'),('Lithuania', 'Lithuania'),('Luxembourg', 'Luxembourg'),('Macao SAR China', 'Macao SAR China'),('Madagascar', 'Madagascar'),('Malawi', 'Malawi'),('Malaysia', 'Malaysia'),('Maldives', 'Maldives'),('Mali', 'Mali'),('Malta', 'Malta'),('Marshall Islands', 'Marshall Islands'),('Martinique', 'Martinique'),('Mauritania', 'Mauritania'),('Mauritius', 'Mauritius'),('Mayotte', 'Mayotte'),('Mexico', 'Mexico'),('Micronesia', 'Micronesia'),('Moldova', 'Moldova'),('Monaco', 'Monaco'),('Mongolia', 'Mongolia'),('Montenegro', 'Montenegro'),('Montserrat', 'Montserrat'),('Morocco', 'Morocco'),('Mozambique', 'Mozambique'),('Myanmar (Burma)', 'Myanmar (Burma)'),('Namibia', 'Namibia'),('Nauru', 'Nauru'),('Nepal', 'Nepal'),('Netherlands', 'Netherlands'),('New Caledonia', 'New Caledonia'),('New Zealand', 'New Zealand'),('Nicaragua', 'Nicaragua'),('Niger', 'Niger'),('Nigeria', 'Nigeria'),('Niue', 'Niue'),('Norfolk Island', 'Norfolk Island'),('North Korea', 'North Korea'),('North Macedonia', 'North Macedonia'),('Northern Mariana Islands', 'Northern Mariana Islands'),('Norway', 'Norway'),('Oman', 'Oman'),('Pakistan', 'Pakistan'),('Palau', 'Palau'),('Palestinian Territories', 'Palestinian Territories'),('Panama', 'Panama'),('Papua New Guinea', 'Papua New Guinea'),('Paraguay', 'Paraguay'),('Peru', 'Peru'),('Philippines', 'Philippines'),('Pitcairn Islands', 'Pitcairn Islands'),('Poland', 'Poland'),('Portugal', 'Portugal'),('Puerto Rico', 'Puerto Rico'),('Qatar', 'Qatar'),('Réunion', 'Réunion'),('Romania', 'Romania'),('Russia', 'Russia'),('Rwanda', 'Rwanda'),('Samoa', 'Samoa'),('San Marino', 'San Marino'),('São Tomé & Príncipe', 'São Tomé & Príncipe'),('Saudi Arabia', 'Saudi Arabia'),('Senegal', 'Senegal'),('Serbia', 'Serbia'),('Seychelles', 'Seychelles'),('Sierra Leone', 'Sierra Leone'),('Singapore', 'Singapore'),('Sint Maarten', 'Sint Maarten'),('Slovakia', 'Slovakia'),('Slovenia', 'Slovenia'),('Solomon Islands', 'Solomon Islands'),('Somalia', 'Somalia'),('South Africa', 'South Africa'),('South Georgia & South Sandwich Islands', 'South Georgia & South Sandwich Islands'),('South Korea', 'South Korea'),('South Sudan', 'South Sudan'),('Spain', 'Spain'),('Sri Lanka', 'Sri Lanka'),('St. Barthélemy', 'St. Barthélemy'),('St. Helena', 'St. Helena'),('St. Kitts & Nevis', 'St. Kitts & Nevis'),('St. Lucia', 'St. Lucia'),('St. Martin', 'St. Martin'),('St. Pierre & Miquelon', 'St. Pierre & Miquelon'),('St. Vincent & Grenadines', 'St. Vincent & Grenadines'),('Sudan', 'Sudan'),('Suriname', 'Suriname'),('Svalbard & Jan Mayen', 'Svalbard & Jan Mayen'),('Sweden', 'Sweden'),('Switzerland', 'Switzerland'),('Syria', 'Syria'),('Taiwan', 'Taiwan'),('Tajikistan', 'Tajikistan'),('Tanzania', 'Tanzania'),('Thailand', 'Thailand'),('Timor-Leste', 'Timor-Leste'),('Togo', 'Togo'),('Tokelau', 'Tokelau'),('Tonga', 'Tonga'),('Trinidad & Tobago', 'Trinidad & Tobago'),('Tunisia', 'Tunisia'),('Turkey', 'Turkey'),('Turkmenistan', 'Turkmenistan'),('Turks & Caicos Islands', 'Turks & Caicos Islands'),('Tuvalu', 'Tuvalu'),('U.S. Outlying Islands', 'U.S. Outlying Islands'),('U.S. Virgin Islands', 'U.S. Virgin Islands'),('Uganda', 'Uganda'),('Ukraine', 'Ukraine'),('United Arab Emirates', 'United Arab Emirates'),('United Kingdom', 'United Kingdom'),('United States', 'United States'),('Uruguay', 'Uruguay'),('Uzbekistan', 'Uzbekistan'),('Vanuatu', 'Vanuatu'),('Vatican City', 'Vatican City'),('Venezuela', 'Venezuela'),('Vietnam', 'Vietnam'),('Wallis & Futuna', 'Wallis & Futuna'),('Western Sahara', 'Western Sahara'),('Yemen', 'Yemen'),('Zambia', 'Zambia'),('Zimbabwe', 'Zimbabwe')]
	
	name = models.CharField(max_length=254)

	speed_class = models.CharField(max_length=254, choices=speed_class_choices)
	IMO = models.CharField(max_length=254)
	vessel_type = models.CharField(max_length=254, choices=vessel_type_choices)
	
	status = models.CharField(max_length=254, choices=status_choices, default='active')
	call_sign = models.CharField(max_length=254)
	flag = models.CharField(max_length=254, choices=country_choices)
	
	gross_tonnage = models.FloatField()
	summer_dwt = models.FloatField()

	length_overall = models.CharField(max_length=254)
	breadth_extreme = models.CharField(max_length=254)
	
	year_built = models.PositiveIntegerField(default=2021, validators=[MinValueValidator(1900), MaxValueValidator(2021)])
	home_port = models.CharField(max_length=254, choices=country_choices)

	is_terminated = models.BooleanField(default=False)

class Charter(models.Model):
	country_choices = [('Afghanistan', 'Afghanistan'),('Åland Islands', 'Åland Islands'),('Albania', 'Albania'),('Algeria', 'Algeria'),('American Samoa', 'American Samoa'),('Andorra', 'Andorra'),('Angola', 'Angola'),('Anguilla', 'Anguilla'),('Antarctica', 'Antarctica'),('Antigua & Barbuda', 'Antigua & Barbuda'),('Argentina', 'Argentina'),('Armenia', 'Armenia'),('Aruba', 'Aruba'),('Australia', 'Australia'),('Austria', 'Austria'),('Azerbaijan', 'Azerbaijan'),('Bahamas', 'Bahamas'),('Bahrain', 'Bahrain'),('Bangladesh', 'Bangladesh'),('Barbados', 'Barbados'),('Belarus', 'Belarus'),('Belgium', 'Belgium'),('Belize', 'Belize'),('Benin', 'Benin'),('Bermuda', 'Bermuda'),('Bhutan', 'Bhutan'),('Bolivia', 'Bolivia'),('Bosnia & Herzegovina', 'Bosnia & Herzegovina'),('Botswana', 'Botswana'),('Bouvet Island', 'Bouvet Island'),('Brazil', 'Brazil'),('British Indian Ocean Territory', 'British Indian Ocean Territory'),('British Virgin Islands', 'British Virgin Islands'),('Brunei', 'Brunei'),('Bulgaria', 'Bulgaria'),('Burkina Faso', 'Burkina Faso'),('Burundi', 'Burundi'),('Cambodia', 'Cambodia'),('Cameroon', 'Cameroon'),('Canada', 'Canada'),('Cape Verde', 'Cape Verde'),('Caribbean Netherlands', 'Caribbean Netherlands'),('Cayman Islands', 'Cayman Islands'),('Central African Republic', 'Central African Republic'),('Chad', 'Chad'),('Chile', 'Chile'),('China', 'China'),('Christmas Island', 'Christmas Island'),('Cocos (Keeling) Islands', 'Cocos (Keeling) Islands'),('Colombia', 'Colombia'),('Comoros', 'Comoros'),('Congo - Brazzaville', 'Congo - Brazzaville'),('Congo - Kinshasa', 'Congo - Kinshasa'),('Cook Islands', 'Cook Islands'),('Costa Rica', 'Costa Rica'),('Côte d’Ivoire', 'Côte d’Ivoire'),('Croatia', 'Croatia'),('Cuba', 'Cuba'),('Curaçao', 'Curaçao'),('Cyprus', 'Cyprus'),('Czechia', 'Czechia'),('Denmark', 'Denmark'),('Djibouti', 'Djibouti'),('Dominica', 'Dominica'),('Dominican Republic', 'Dominican Republic'),('Ecuador', 'Ecuador'),('Egypt', 'Egypt'),('El Salvador', 'El Salvador'),('Equatorial Guinea', 'Equatorial Guinea'),('Eritrea', 'Eritrea'),('Estonia', 'Estonia'),('Eswatini', 'Eswatini'),('Ethiopia', 'Ethiopia'),('Falkland Islands', 'Falkland Islands'),('Faroe Islands', 'Faroe Islands'),('Fiji', 'Fiji'),('Finland', 'Finland'),('France', 'France'),('French Guiana', 'French Guiana'),('French Polynesia', 'French Polynesia'),('French Southern Territories', 'French Southern Territories'),('Gabon', 'Gabon'),('Gambia', 'Gambia'),('Georgia', 'Georgia'),('Germany', 'Germany'),('Ghana', 'Ghana'),('Gibraltar', 'Gibraltar'),('Greece', 'Greece'),('Greenland', 'Greenland'),('Grenada', 'Grenada'),('Guadeloupe', 'Guadeloupe'),('Guam', 'Guam'),('Guatemala', 'Guatemala'),('Guernsey', 'Guernsey'),('Guinea', 'Guinea'),('Guinea-Bissau', 'Guinea-Bissau'),('Guyana', 'Guyana'),('Haiti', 'Haiti'),('Heard & McDonald Islands', 'Heard & McDonald Islands'),('Honduras', 'Honduras'),('Hong Kong SAR China', 'Hong Kong SAR China'),('Hungary', 'Hungary'),('Iceland', 'Iceland'),('India', 'India'),('Indonesia', 'Indonesia'),('Iran', 'Iran'),('Iraq', 'Iraq'),('Ireland', 'Ireland'),('Isle of Man', 'Isle of Man'),('Israel', 'Israel'),('Italy', 'Italy'),('Jamaica', 'Jamaica'),('Japan', 'Japan'),('Jersey', 'Jersey'),('Jordan', 'Jordan'),('Kazakhstan', 'Kazakhstan'),('Kenya', 'Kenya'),('Kiribati', 'Kiribati'),('Kuwait', 'Kuwait'),('Kyrgyzstan', 'Kyrgyzstan'),('Laos', 'Laos'),('Latvia', 'Latvia'),('Lebanon', 'Lebanon'),('Lesotho', 'Lesotho'),('Liberia', 'Liberia'),('Libya', 'Libya'),('Liechtenstein', 'Liechtenstein'),('Lithuania', 'Lithuania'),('Luxembourg', 'Luxembourg'),('Macao SAR China', 'Macao SAR China'),('Madagascar', 'Madagascar'),('Malawi', 'Malawi'),('Malaysia', 'Malaysia'),('Maldives', 'Maldives'),('Mali', 'Mali'),('Malta', 'Malta'),('Marshall Islands', 'Marshall Islands'),('Martinique', 'Martinique'),('Mauritania', 'Mauritania'),('Mauritius', 'Mauritius'),('Mayotte', 'Mayotte'),('Mexico', 'Mexico'),('Micronesia', 'Micronesia'),('Moldova', 'Moldova'),('Monaco', 'Monaco'),('Mongolia', 'Mongolia'),('Montenegro', 'Montenegro'),('Montserrat', 'Montserrat'),('Morocco', 'Morocco'),('Mozambique', 'Mozambique'),('Myanmar (Burma)', 'Myanmar (Burma)'),('Namibia', 'Namibia'),('Nauru', 'Nauru'),('Nepal', 'Nepal'),('Netherlands', 'Netherlands'),('New Caledonia', 'New Caledonia'),('New Zealand', 'New Zealand'),('Nicaragua', 'Nicaragua'),('Niger', 'Niger'),('Nigeria', 'Nigeria'),('Niue', 'Niue'),('Norfolk Island', 'Norfolk Island'),('North Korea', 'North Korea'),('North Macedonia', 'North Macedonia'),('Northern Mariana Islands', 'Northern Mariana Islands'),('Norway', 'Norway'),('Oman', 'Oman'),('Pakistan', 'Pakistan'),('Palau', 'Palau'),('Palestinian Territories', 'Palestinian Territories'),('Panama', 'Panama'),('Papua New Guinea', 'Papua New Guinea'),('Paraguay', 'Paraguay'),('Peru', 'Peru'),('Philippines', 'Philippines'),('Pitcairn Islands', 'Pitcairn Islands'),('Poland', 'Poland'),('Portugal', 'Portugal'),('Puerto Rico', 'Puerto Rico'),('Qatar', 'Qatar'),('Réunion', 'Réunion'),('Romania', 'Romania'),('Russia', 'Russia'),('Rwanda', 'Rwanda'),('Samoa', 'Samoa'),('San Marino', 'San Marino'),('São Tomé & Príncipe', 'São Tomé & Príncipe'),('Saudi Arabia', 'Saudi Arabia'),('Senegal', 'Senegal'),('Serbia', 'Serbia'),('Seychelles', 'Seychelles'),('Sierra Leone', 'Sierra Leone'),('Singapore', 'Singapore'),('Sint Maarten', 'Sint Maarten'),('Slovakia', 'Slovakia'),('Slovenia', 'Slovenia'),('Solomon Islands', 'Solomon Islands'),('Somalia', 'Somalia'),('South Africa', 'South Africa'),('South Georgia & South Sandwich Islands', 'South Georgia & South Sandwich Islands'),('South Korea', 'South Korea'),('South Sudan', 'South Sudan'),('Spain', 'Spain'),('Sri Lanka', 'Sri Lanka'),('St. Barthélemy', 'St. Barthélemy'),('St. Helena', 'St. Helena'),('St. Kitts & Nevis', 'St. Kitts & Nevis'),('St. Lucia', 'St. Lucia'),('St. Martin', 'St. Martin'),('St. Pierre & Miquelon', 'St. Pierre & Miquelon'),('St. Vincent & Grenadines', 'St. Vincent & Grenadines'),('Sudan', 'Sudan'),('Suriname', 'Suriname'),('Svalbard & Jan Mayen', 'Svalbard & Jan Mayen'),('Sweden', 'Sweden'),('Switzerland', 'Switzerland'),('Syria', 'Syria'),('Taiwan', 'Taiwan'),('Tajikistan', 'Tajikistan'),('Tanzania', 'Tanzania'),('Thailand', 'Thailand'),('Timor-Leste', 'Timor-Leste'),('Togo', 'Togo'),('Tokelau', 'Tokelau'),('Tonga', 'Tonga'),('Trinidad & Tobago', 'Trinidad & Tobago'),('Tunisia', 'Tunisia'),('Turkey', 'Turkey'),('Turkmenistan', 'Turkmenistan'),('Turks & Caicos Islands', 'Turks & Caicos Islands'),('Tuvalu', 'Tuvalu'),('U.S. Outlying Islands', 'U.S. Outlying Islands'),('U.S. Virgin Islands', 'U.S. Virgin Islands'),('Uganda', 'Uganda'),('Ukraine', 'Ukraine'),('United Arab Emirates', 'United Arab Emirates'),('United Kingdom', 'United Kingdom'),('United States', 'United States'),('Uruguay', 'Uruguay'),('Uzbekistan', 'Uzbekistan'),('Vanuatu', 'Vanuatu'),('Vatican City', 'Vatican City'),('Venezuela', 'Venezuela'),('Vietnam', 'Vietnam'),('Wallis & Futuna', 'Wallis & Futuna'),('Western Sahara', 'Western Sahara'),('Yemen', 'Yemen'),('Zambia', 'Zambia'),('Zimbabwe', 'Zimbabwe')]
	
	ship = models.ForeignKey(Ship, on_delete=models.SET_NULL, null=True)

	captain = models.ForeignKey(Crew, related_name='captain', on_delete=models.SET_NULL, null=True) #TODO make validation so that u can only make captain for captain position crew
	
	chief_mate = models.ForeignKey(Crew, related_name='chief_mate', on_delete=models.SET_NULL, null=True)
	second_mate = models.ForeignKey(Crew, related_name='second_mate', on_delete=models.SET_NULL, null=True)
	third_mate = models.ForeignKey(Crew, related_name='third_mate', on_delete=models.SET_NULL, null=True)
	deck_cadet = models.ManyToManyField(Crew, related_name='deck_cadet')
	chief_engineer = models.ForeignKey(Crew, related_name='chief_engineer', on_delete=models.SET_NULL, null=True)
	second_engineer = models.ForeignKey(Crew, related_name='second_engineer', on_delete=models.SET_NULL, null=True)
	third_engineer = models.ForeignKey(Crew, related_name='third_engineer', on_delete=models.SET_NULL, null=True)
	fourth_engineer = models.ForeignKey(Crew, related_name='fourth_engineer', on_delete=models.SET_NULL, null=True)
	engine_cadet = models.ManyToManyField(Crew, related_name='engine_cadet')
	electrician = models.ManyToManyField(Crew, related_name='electrician')
	boatswain = models.ForeignKey(Crew, related_name='boatswain', on_delete=models.SET_NULL, null=True)
	pump_man = models.ManyToManyField(Crew, related_name='pump_man')
	able_bodied_seaman = models.ManyToManyField(Crew, related_name='able_bodied_seaman')
	ordinary_seaman = models.ManyToManyField(Crew, related_name='ordinary_seaman')
	fitter = models.ManyToManyField(Crew, related_name='fitter')
	oiler = models.ManyToManyField(Crew, related_name='oiler')
	wiper = models.ManyToManyField(Crew, related_name='wiper')
	chief_cook = models.ManyToManyField(Crew, related_name='chief_cook')
	steward = models.ManyToManyField(Crew, related_name='steward')

	description = models.TextField()
	from_place = models.CharField(max_length=254, choices=country_choices)
	to_place = models.CharField(max_length=254, choices=country_choices)
	from_datetime = models.DateTimeField()
	to_datetime = models.DateTimeField()

	
	def distance(self):
		def findGeocode(country):
			try:
				geolocator = Nominatim(user_agent="your_app_name")
				return geolocator.geocode(country)
			except GeocoderTimedOut:
				return findGeocode(country)
		location1 = findGeocode(self.from_place)
		location2 = findGeocode(self.to_place)
		coords1 = (location1.latitude, location2.longitude)
		coords2 = (location2.latitude, location2.longitude)
		dist = geopy.distance.vincenty(coords1, coords2).km
		return dist

	def eta(self):
		distance = self.distance()
		speed_class = {'Normal (23 Knots)': 23, 'Slow Streaming (19 Knots)': 19,
			 'Extra Slow Streaming (16.5 Knots)': 16.5, 'Minimal Costs (13.5 Knots)': 13.5}
		speed = speed_class[self.ship.speed_class]
		speed *= 1.852
		hours = distance / speed
		return hours

	def income(self):
		return self.distance() * 10

