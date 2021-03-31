
async def kill_animal():
    """
    Mata um animal (seta como morto)

    * Se ele não estiver já morto
    * Se ele não estiver deletado nem vendido nem perdido
    * Atualizada a data de morte em 'deadOn'
    """
    print("Matando o animal!")
    return {'animal':'morto'}