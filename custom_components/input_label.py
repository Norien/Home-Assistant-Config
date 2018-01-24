"""
@ Author      : Suresh Kalavala
@ Date        : 09/14/2017
@ Description : Input Label  - A label that holds data

@ Notes:        Copy this file and services.yaml files and place it in your 
                "Home Assistant Config folder\custom_components\" folder

                To use the component, have the following in your .yaml file:
                The 'value' is optional, by default, it is set to 0 

input_label:
  some_string1:
    name: Some String 1 
    icon: mdi:alphabetical

  input_label:
    name: Some String 2
    value: 'Hello, Home Assistant!'
    icon: mdi:alphabetical

"""

"""
Component to provide input_label.

For more details about this component, please contact Suresh Kalavala
"""
import asyncio
import logging
import os

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.config import load_yaml_config_file
from homeassistant.const import (ATTR_ENTITY_ID, CONF_ICON, CONF_NAME)
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.restore_state import async_get_last_state
from homeassistant.loader import bind_hass

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'input_label'
ENTITY_ID_FORMAT = DOMAIN + '.{}'

ATTR_VALUE   = "value"
DEFAULT_VALUE = "not set"

ATTR_READONLY  = "readonly"
DEFAULT_READONLY = False
DEFAULT_ICON = "mdi:label"

SERVICE_SETNAME = 'set_name'
SERVICE_SETVALUE = 'set_value'
SERVICE_SETICON = 'set_icon'

SERVICE_SCHEMA = vol.Schema({
    vol.Optional(ATTR_ENTITY_ID): cv.entity_ids,
    vol.Optional(ATTR_VALUE): cv.string,
    vol.Optional(ATTR_READONLY): cv.boolean,
    vol.Optional(CONF_ICON): cv.icon,
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        cv.slug: vol.Any({
            vol.Optional(CONF_ICON, default=DEFAULT_ICON): cv.icon,
            vol.Optional(ATTR_VALUE, default=DEFAULT_VALUE): cv.string,
            vol.Optional(ATTR_READONLY, default=DEFAULT_READONLY): cv.boolean,
            vol.Optional(CONF_NAME): cv.string,
        }, None)
    })
}, extra=vol.ALLOW_EXTRA)

@bind_hass
def set_value(hass, entity_id, value, readonly, icon):
    hass.add_job(async_set_value, hass, entity_id, value, readonly)

@bind_hass
def set_icon(hass, entity_id, icon):
    hass.add_job(async_set_icon, hass, entity_id, icon)


@bind_hass
def set_name(hass, entity_id, name):
    hass.add_job(async_set_icon, hass, entity_id, name)

@callback
@bind_hass
def async_set_value(hass, entity_id, value, readonly, icon):
    hass.async_add_job(hass.services.async_call(
        DOMAIN, SERVICE_SETVALUE, {ATTR_ENTITY_ID: entity_id, ATTR_VALUE: value, ATTR_READONLY: readonly}))

@callback
@bind_hass
def async_set_icon(hass, entity_id, icon):
    hass.async_add_job(hass.services.async_call(
        DOMAIN, SERVICE_SETICON, {ATTR_ENTITY_ID: entity_id, CONF_ICON: icon}))

@callback
@bind_hass
def async_set_name(hass, entity_id, name):
    hass.async_add_job(hass.services.async_call(
        DOMAIN, SERVICE_SETICON, {ATTR_ENTITY_ID: entity_id, CONF_NAME: name}))

@asyncio.coroutine
def async_setup(hass, config):
    """Set up a input_label."""
    component = EntityComponent(_LOGGER, DOMAIN, hass)

    entities = []

    for object_id, cfg in config[DOMAIN].items():
        if not cfg:
            cfg = {}

        name = cfg.get(CONF_NAME)
        value = cfg.get(ATTR_VALUE)
        icon = cfg.get(CONF_ICON)
        readonly = cfg.get(ATTR_READONLY)

        entities.append(GlobalLabelData(object_id, name, value, icon, readonly))

    if not entities:
        return False

    @asyncio.coroutine
    def async_handler_service(service):
        """Handle a call to the input_label services."""
        target_global_labels = component.async_extract_from_service(service)

        if service.service == SERVICE_SETVALUE:
            attr = 'async_set_value'
        elif service.service == SERVICE_SETNAME:
            attr = 'async_set_name'
        else:
            attr = "async_set_icon"

        tasks = [getattr(global_label, attr)(service.data[ATTR_VALUE]) 
                  for global_label in target_global_labels]
        if tasks:
            yield from asyncio.wait(tasks, loop=hass.loop)

    descriptions = yield from hass.async_add_job(
        load_yaml_config_file, os.path.join(
            os.path.dirname(__file__), 'services.yaml')
    )

    hass.services.async_register(
        DOMAIN, SERVICE_SETVALUE, async_handler_service,
        schema=SERVICE_SCHEMA)

    hass.services.async_register(
        DOMAIN, SERVICE_SETICON, async_handler_service,
        schema=SERVICE_SCHEMA)

    hass.services.async_register(
        DOMAIN, SERVICE_SETNAME, async_handler_service,
        schema=SERVICE_SCHEMA)

    yield from component.async_add_entities(entities)
    return True


class GlobalLabelData(Entity):
    """Representation of a input_label."""

    def __init__(self, object_id, name, value, icon, readonly):
        """Initialize a input_label."""
        self.entity_id = ENTITY_ID_FORMAT.format(object_id)
        self._name = name
        self._state = value
        self._readonly = readonly
        self._icon = icon
 
    @property
    def should_poll(self):
        """If entity should be polled."""
        return False

    @property
    def name(self):
        """Return name of the input_label."""
        return self._name

    @property
    def icon(self):
        """Return the icon to be used for this entity."""
        return self._icon

    @property
    def readonly(self):
        """Return the readony property of this entity."""
        return self._readonly

    @property
    def state(self):
        """Return the current value of the input_label."""
        return self._state

    @property
    def state_attributes(self):
        """Return the state attributes."""
        return {
            ATTR_VALUE: self._state,
        }

    @asyncio.coroutine
    def async_added_to_hass(self):
        """Call when entity about to be added to Home Assistant."""
        # If not None, we got an initial value.
        if self._state is not None:
            return

        state = yield from async_get_last_state(self.hass, self.entity_id)
        self._state = state and state.state == state

    @asyncio.coroutine
    def async_set_name(self, name):
        self._name = name
        yield from self.async_update_ha_state()

    @asyncio.coroutine
    def async_set_icon(self, icon):
        self._icon = icon
        yield from self.async_update_ha_state()

    @asyncio.coroutine
    def async_set_value(self, value):
        try:
            if not self._readonly:
                self._state = value
            else:
                _LOGGER.warning("The input label '%s'is marked as readonly. A new value cannot be set.", 
                    self.entity_id)
        except:
            _LOGGER.error("Error: '%s' is not in a valid string format.", value)
        yield from self.async_update_ha_state()