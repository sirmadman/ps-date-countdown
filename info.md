## How it works
This script creates a sensor that a counts down to the next occurrance of a date, like a birthday or anniversary and gives the number of years as an attribute

Requires `python_script:` to be enabled in you configuration

## Installation
Copy the Python script in to your `/config/python_scripts` directory or install via HACS.

## Script arguments
key | required | type | description
-- | -- | -- | --
`name:` | True | string | Name of the date (eg. John)
`type:` | True | string | Type of date (eg. Birthday)
`date:` | True | string | Date, in format DD/MM/YYYY
`date_format:` | False | string | Date format, according to Python's strptime() like %y-%m-%d. `date`should then be in entered in this format.
`friendly_name:` | False | string | Name to display. If not set it will be set with logic.

The date can be in the future if you want to countdown to the date itself, and then the anniversaries thereafter.

## Usage
Each sensor **requires**:

```
name: NAME_OF_DATE
type: TYPE_OF_DATE
date: DD/MM/YYYY_OF DATE
```

optional:

```
friendly_name: 'Our yearly reminder'
date_format: %y-%m-%d
```
If `date_format` is set `date` must be according to that format. Example according to format above:

```
date: YYYY-MM-DD
```

examples:

```
name: John
type: birthday
date: 17/08/1971
```

or

```
name: Our wedding
type: anniversary
date: 14/02/1994
```

## Generated sensors
Each sensor is given the following automatically:

```
entity_id: sensor.<type>_<name>
friendly_name: <name> <type>
state: <Days to the date from today>
nextoccur: <Date of next occurance>
nextoccur_iso8601: <Date of next occurance in ISO 8601 format (YYYY-MM-DD)>
nextoccur_datetime: <Date object of next occurance>
years: <Number of years it will be>
```

So, the two sensors we created above would come out as:

```
sensor.birthday_john
friendly_name: John’s birthday
state: However many days it is until 17th August
nextoccur: 17/08/YYYY (either this year or next year as appropriate)
nextoccur_iso8601: YYYY-08-17 (either this year or next year as appropriate)
nextoccur_datetime: dateObject (either this year or next year as appropriate)
years: However old John will be on his next birthday

sensor.anniversary_our_wedding
friendly_name: Our wedding anniversary
state: However many days to 14th February
nextoccur: 14/02/YYYY (either this year or next year as appropriate)
nextoccur_iso8601: YYYY-02-14 (either this year or next year as appropriate)
nextoccur_datetime: dateObject (either this year or next year as appropriate)
years: How many years you will have been married on that day
```

Note that if the type is 'birthday' the sensor will automatically add an apostrophe if not `date_format` is supplied.

## Example configuration.yaml entry
An example automation to create and refresh the above two sensors daily would be:

```yaml
automation:
  - alias: Reminder - Refresh date countdown sensors
    trigger:
      - platform: time
        at: '00:00:01'
      - platform: homeassistant
        event: start
    action:
      - service: python_script.date_countdown
        data:
          name: John
          type: birthday
          date: 17/08/1971
      - service: python_script.date_countdown
        data:
          name: Our wedding
          type: anniversary
          date: 14/02/1994
```

## Example automation
An example automation to remind you of an event 7 days before it occurs would be:

```yaml
automation:
  - alias: Reminder - John's birthday is coming up
    trigger:
      - platform: state
        entity_id: sensor.birthday_john
        to: '7'
    action:
      - wait_template: "{{ states('sensor.time') == '10:00' }}"
      - service: notify.notify
        data:
          message: "John's birthday is only a week away!"
```

## Example Lovelace representation
Utilising the attributes provided and the [custom lovelace card](https://github.com/custom-cards/secondaryinfo-entity-row) for adding secondary info to an entity row. 

```yaml
type: entities
show_header_toggle: false
title: Our Events
entities:
  - entity: sensor.anniversary_our_wedding
    secondary_info: '[[ {entity}.attributes.nextoccur ]]  ( [[ {entity}.attributes.years ]] Years )'
    type: 'custom:secondaryinfo-entity-row'
```

Will provide the following lovelace representation:

![Lovelace example](https://community-home-assistant-assets.s3.dualstack.us-west-2.amazonaws.com/original/3X/b/a/ba44600d7f41b1525a3c835d11bcc3bd59815b23.png)

{% if installed %}
## Changes as compared to your installed version:

### Breaking Changes

### Changes

### Features

{% if version_installed.replace("v", "").replace(".","") | int < 4.0  %}
- Added `date_format:` - Date format, according to Python's strptime() like %y-%m-%d. `date`should then be in entered in this format.
- Added `friendly_name:` - Name to display instead of automatically set.
{% endif %}

### Bugfixes
---
{% endif %}
