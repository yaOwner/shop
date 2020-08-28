@client.command()
@commands.has_permissions(administrator = True)
async def add_role(ctx, role: discord.Role = None, cost: int = None, ids = None):
		
	if role is None:
		emb = discord.Embed(description = f'Укажите роль, которую хотите добавить в магазин!')
		emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))

		await ctx.send(embed = emb)	

	else:
		if cost is None:
			emb = discord.Embed(description = f'Укажите стоимость роли!')
			emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))

			await ctx.send(embed = emb)	
				
		elif cost < 1:
			emb = discord.Embed(description = f'Стоимость роли не может быть такой низкой !')
			emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))

			await ctx.send(embed = emb)

		elif ids is None:
			emb = discord.Embed(description = 'Укажите Key для покупки роли!')
			emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))

			await ctx.send(embed = emb)	
				
		else:
			cursor.execute("INSERT INTO testshop3 VALUES ({}, {}, {}, {})".format(role.id, ctx.guild.id, cost, ids))
			connection.commit()

			await ctx.message.add_reaction('✅')
					
			await asyncio.sleep(5)
			await ctx.message.delete()


@client.command()
@commands.has_permissions(administrator = True)
async def remove_role(ctx, role: discord.Role = None):

	if role is None:
		emb = discord.Embed(description = f'Укажите роль, которую хотите удалить из магазина!')
		emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))

		await ctx.send(embed = emb)	

	else:
		cursor.execute("DELETE FROM testshop3 WHERE role_id = {}".format(role.id))
		connection.commit()

		await ctx.message.add_reaction('✅')
				
		await asyncio.sleep(5)
		await ctx.message.delete()

@client.command()
async def shop(ctx):

	embed = discord.Embed(title = f'Магазин ролей сервера {ctx.guild}:\nㅤㅤㅤ')

	counter = 0
	for row in cursor.execute("SELECT * FROM testshop3 WHERE id = {} ORDER BY cost DESC".format(ctx.guild.id)):
		if ctx.guild.get_role(row[0]) != None:
			if ctx.guild.get_role(row[0]) in ctx.author.roles:

				embed.add_field(
					name = f'| Куплено', 
					value = f'| {ctx.guild.get_role(row[0]).mention}\nㅤㅤㅤ'
				)

			else:

				counter += 1
										
				embed.add_field(
					name = f'| [{row[3]}]   > <a:currency:737351940320657588> {row[2]}', 
					value = f'| {ctx.guild.get_role(row[0]).mention}\nㅤㅤㅤ'
				)

	await ctx.message.delete()
	embed.set_footer(text = 'Страница 1 из 1 | Напишите `=buy_role <key>` для покупки роли. Пример - `=buy_role 1`')
	await ctx.send(embed = embed)


@client.command()
async def buy_role(ctx, ids = None):
		
	if ids is None:
		emb = discord.Embed(description = f'Укажите роль, которую хотите приобрести!')
		emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))

		await ctx.send(embed = emb)	

	else:
							
		try:
			if cursor.execute("SELECT cost FROM testshop3 WHERE ids = {}".format(ids)).fetchone()[0] > cursor.execute("SELECT cash FROM test24 WHERE id = {} ".format(ctx.author.id)).fetchone()[0]:
				emb = discord.Embed(description = f'У вас недостаточно денег! Не хватает <a:currency:737351940320657588> {cursor.execute("SELECT cost FROM testshop3 WHERE ids = {}".format(ids)).fetchone()[0] - cursor.execute("SELECT cash FROM test24 WHERE id = {}".format(ctx.author.id)).fetchone()[0]}', colour = 0xe74c3c)
				emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))

				await ctx.send(embed = emb)


			else:

				for row in cursor.execute("SELECT * FROM testshop3 WHERE ids = {}".format(ids)):
					if ctx.guild.get_role(row[0]) in ctx.author.roles:
						await message.delete()

						emb = discord.Embed(description = 'У вас уже есть такая роль!')
						emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))

						await ctx.send(embed = emb)

					else:

						await message.delete()

						role = discord.utils.get(ctx.guild.roles, id = row[0])
						await ctx.author.add_roles(role)

						emb = discord.Embed(description = f'Вы успешно приобрели роль {ctx.guild.get_role(row[0]).mention}')
						emb.set_author(icon_url = '{}'.format(ctx.author.avatar_url), name = '{}'.format(ctx.author))

						await ctx.send(embed = emb)

						cursor.execute("UPDATE test24 SET cash = cash - {} WHERE id = {}".format(cursor.execute("SELECT cost FROM testshop3 WHERE ids = {}".format(ids)).fetchone()[0], ctx.author.id))
						connection.commit()
						   
		except:
			await ctx.send(f'Обработка... Если ответа не последует, указан неверный id предмета [buy_role {ids}]')
