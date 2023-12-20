# from swgoh_comlink import SwgohComlink

SWGOH_GG = "swgoh.gg"


class SWGOH():
    def __init__(self, swgoh_info, ally_code):
        self.comlink = None
        self.player_data = dict()
        self.player_data["name"] = "Loreck Avery"
        self.player_data["guildID"] = None
        # guild_id = self.player_data['guildId']
        # self.comlink = SwgohComlink()
        # self.player_data = self.comlink.get_player(ally_code)

    @staticmethod
    def get_swgoh_site(use_swgoh_gg, alt_swgoh_gg):
        if (use_swgoh_gg and len(alt_swgoh_gg) > 0):
            raise Exception("Cannot set both")
        if use_swgoh_gg:
            return SWGOH_GG
        return alt_swgoh_gg

    def get(self, keys):
        """
        Return dictionary of keys from SWGOH game.

        Uses different APIs depending on the requested information. Use
        swgoh.gg whenever possible.
        """
        ret_dict = dict()
        for key in keys:
            if key == "name":
                ret_dict[key] = self.__get_name()
            if key == "clan":
                ret_dict[key] = self.__get_clan()

        return ret_dict

    def __get_name(self):
        """
        Use SWGOH Comlink - https://github.com/swgoh-utils/swgoh-comlink
        """
        return "Loreck Avery"
        # return self.player_data['name']

    def __get_clan(self):
        """
        Use SWGOH Comlink - https://github.com/swgoh-utils/swgoh-comlink
        """
        return "Dejarik"
        # guild_id = self.player_data['guildId']
        # guild = self.comlink.get_guild(guild_id)
        # return guild['profile']['name']
