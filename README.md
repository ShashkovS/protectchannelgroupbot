# Бот позволяет запретить добавляться в группу, привязанную к чату, и писать вне комментов

Решение здесь, к сожалению, не такое простое, как может быть бы хотелось.
Идея вот в чём.

1. В настройках группы нужно убедиться, что отправлять сообщения могут не только участники.
2. Далее если начать писать комментарий к посту в канале, то добавления в группу не происходит. И писать можно только комменты к сообщениям в канале.
3. Но тем или иным способом можно добавиться в чат-группу, и тогда можно писать сообщения там.
4. Идея в том, чтобы всех, кто туда добавляется, удалять оттуда и разбанивать обратно
5. Бот https://t.me/protectchannelgroupbot это делает. Его нужно добавить админом в чат-группу канала.
6. Но есть нюанс. Это будет работать только с новодобавляющимися пользователями.
7. Со старыми есть сложность. Их можно удалить из группы из-под админа, но это их забанит, то есть лишит возможности писать комменты.
8. Разбанить назад чёт непросто. Но без этого они не смогут комментировать.

![1](https://raw.githubusercontent.com/ShashkovS/protectchannelgroupbot/main/docs/01_grp_admin.png)
![2](https://raw.githubusercontent.com/ShashkovS/protectchannelgroupbot/main/docs/02_grp_type.png)
![3](https://raw.githubusercontent.com/ShashkovS/protectchannelgroupbot/main/docs/03_grp_privacy.png)
![4](https://raw.githubusercontent.com/ShashkovS/protectchannelgroupbot/main/docs/04_grp_admin.png)
![5](https://raw.githubusercontent.com/ShashkovS/protectchannelgroupbot/main/docs/05_grp_addbot.png)
![6](https://raw.githubusercontent.com/ShashkovS/protectchannelgroupbot/main/docs/01_grp_admin.png)
![7](https://raw.githubusercontent.com/ShashkovS/protectchannelgroupbot/main/docs/06_bot_auth.png)
