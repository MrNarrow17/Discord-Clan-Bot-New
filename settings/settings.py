from typing import Any

import discord
import revampDB

db = revampDB.database("settings.db", mode=True)


class Settings:
    def read_settings(self, server: discord.Guild, key: str) -> Any:
        data = db.ReadDatabase(server.id)

        if not isinstance(data, dict):
            return None

        return data.get(key)

    def write_settings(self, server: discord.Guild, key: str, value: Any) -> None:
        data = db.ReadDatabase(server.id)

        if not isinstance(data, dict):
            data = {}

        data[key] = value

        db.WriteDatabase(data, server.id)
