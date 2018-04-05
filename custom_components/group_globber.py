import asyncio

import fnmatch
import re

import logging
import voluptuous as vol

from homeassistant.helpers import config_validation as cv
from homeassistant.const import (
    EVENT_STATE_CHANGED)
from homeassistant.components import (
    group)

import homeassistant.core as ha

DOMAIN = 'group_globber'

_LOGGER = logging.getLogger(__name__)

CONF_GROUPS = 'groups'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_GROUPS): vol.Schema({
            str: vol.Schema(vol.All(cv.ensure_list, [cv.string]))
        })
    })
}, extra=vol.ALLOW_EXTRA)

@asyncio.coroutine
def async_setup(hass, config):

    #lock = threading.Lock()
    config = config.get(DOMAIN)
    groups = config.get(CONF_GROUPS)

    # We are going to keep track of what we see, so we don't have to check the groups
    # on every state update.
    seen = set()

    for key, value in groups.items():
        groups[key] = [re.compile(fnmatch.translate(x)) for x in value]

    @ha.callback
    def _handle_state_change(event):

        entity_id = event.data.get('entity_id')
        domain, object_id = ha.split_entity_id(entity_id)

        if domain == 'group':

            # Newly created group won't have an old_state
            is_new = event.data.get('old_state') is None
            if is_new:
                #_LOGGER.debug("Group %s created", entity_id)

                group_id = entity_id
                expressions = groups.get(group_id)

                if expressions:
                    # We have to get all the items and then see if they match. Seems
                    # like it could be rather expensive if we had a lot of groups created (reloaded).
                    # Maybe I'm micro-optimizing...
                    for entity_id in hass.states.async_entity_ids():
                        seen.add(entity_id)
                        if any(x.match(entity_id) for x in expressions):
                            _LOGGER.debug("Adding %s to group %s (reload)", entity_id, group_id)
                            group.set_group(hass, object_id, add=[entity_id])

        else:
            # Check that we have a state. If it isn't there, that means it is a
            # probably being removed
            new_state = event.data.get('new_state')
            if new_state:

                if not entity_id in seen:
                    seen.add(entity_id)

                    for group_id, expressions in groups.items():
                        if any(x.match(entity_id) for x in expressions):
                            _LOGGER.debug("Adding %s to group %s (state_change)", entity_id, group_id)
                            _, object_id = ha.split_entity_id(group_id)
                            group.set_group(hass, object_id, add=[entity_id])
                return

            # If we get here, that means we didn't have a new_state, so that means it was removed
            if entity_id in seen:
                seen.remove(entity_id)

    hass.bus.async_listen(EVENT_STATE_CHANGED, _handle_state_change)
    return True