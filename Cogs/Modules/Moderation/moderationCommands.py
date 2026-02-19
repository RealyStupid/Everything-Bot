from Utilities.cogDeps import *

class ModerationCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Create custom group (not auto-registered)
        self.mod_group = create_group(
            name="moderation",
            description="These commands are related to server moderation."
        )

        # Add subcommands
        self.mod_group.add_command(
            app_commands.Command(
                name="say",
                description="Make the bot say a message.",
                callback=self.sayMessage,
            )
        )

        self.mod_group.add_command(
            app_commands.Command(
                name="kick",
                description="Kick a member from the server.",
                callback=self.kickMember,
            )
        )

    @module("moderation")
    @guilds_for()
    async def sayMessage(self, interaction: discord.Interaction, message: str):
        """Make the bot say a message."""
        await interaction.response.send_message(message)

    @module("moderation")
    @guilds_for()
    async def kickMember(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        """Kick a member from the server."""
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.mention} has been kicked. Reason: {reason}")

    @module("moderation")
    @guilds_for()
    async def banMember(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        """Ban a member from the server."""
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member.mention} has been banned. Reason: {reason}")

    @module("moderation")
    @guilds_for()
    async def unbanMember(self, interaction: discord.Interaction, user: discord.User):
        """Unban a member from the server."""
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"{user.mention} has been unbanned.")

    @module("moderation")
    @guilds_for()
    async def warnMember(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        """Warn a member in the server."""
        # This is a placeholder for warning logic (e.g., storing warnings in a database)
        await interaction.response.send_message(f"{member.mention} has been warned. Reason: {reason}")

async def setup(bot):
    await bot.add_cog(ModerationCommands(bot))
