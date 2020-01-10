today = datetime.datetime.now().date()

name = data.get('name')
type = data.get('type')
sensorName = "sensor.{}_{}".format(type , name.replace(" " , "_"))
friendly_name = data.get('friendly_name', '')

dateFormat = data.get('date_format')

dateStr = data.get('date')
if dateFormat is not None:
  try:
    date = datetime.strptime(dateStr, dateFormat)
    dateYear = date.year
    dateMonth = date.month
    dateDay = date.day
  except ValueError as ve:
    raise ParseException(s, l, str(ve))

try: date
except NameError:
  dateSplit = dateStr.split("/")

  dateDay = int(dateSplit[0])
  dateMonth = int(dateSplit[1])
  dateYear =  int(dateSplit[2])
  date = datetime.date(dateYear , dateMonth , dateDay)

thisYear = today.year
nextOccur = datetime.date(thisYear , dateMonth , dateDay)

numberOfDays = 0
years = int(thisYear) - dateYear

if today < nextOccur:
  numberOfDays = (nextOccur - today).days

elif today > nextOccur:
  if thisYear > dateYear + 1:
    nextOccur = datetime.date(thisYear + 1 , dateMonth , dateDay)
    numberOfDays = (nextOccur - today).days
    years = years + 1
  else:
    nextOccur = datetime.date(dateYear , dateMonth , dateDay)
    numberOfDays = (nextOccur - today).days
    years = years + 1

if not friendly_name:
  if type.lower() == 'birthday':
    friendly_name = "{}'s {}".format(name , type)
  else:
    friendly_name = "{} {}".format(name , type)

hass.states.set(sensorName , numberOfDays ,
  {
    "icon" : "mdi:calendar-star" ,
    "unit_of_measurement" : "days" ,
    "friendly_name" : friendly_name,
    "nextoccur" : "{}/{}/{}".format(nextOccur.day , nextOccur.month , nextOccur.year) ,
    "nextoccur_iso8601" : "{}-{}-{}".format(nextOccur.year , nextOccur.month , nextOccur.day) ,
    "nextoccur_datetime" : nextOccur
    "years" : years
  }
)
