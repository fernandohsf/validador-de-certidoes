# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:/Projetos Python/Verificador de certidões negativas/AnaliseCertidoes.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Program Files/Python311/Lib/site-packages/fitz', 'fitz/'), ('C:/Program Files/Python311/Lib/site-packages/openpyxl', 'openpyxl/'), ('C:/Program Files/Python311/Lib/site-packages/xlsxwriter', 'xlsxwriter/'), ('D:/Projetos Python/Verificador de certidões negativas/CadastroProfessorFormador.csv', '.')],
    hiddenimports=['glob', 'MunicipiosPR.AnaliseAlmiranteTamandare', 'MunicipiosPR.AnaliseAndira', 'MunicipiosPR.AnaliseApucarana', 'MunicipiosPR.AnaliseArapongas', 'MunicipiosPR.AnaliseArapoti', 'MunicipiosPR.AnaliseBarbosaFerraz', 'MunicipiosPR.AnaliseBelaVistaDoParaiso', 'MunicipiosPR.AnaliseBoaVenturaDeSaoRoque', 'MunicipiosPR.AnaliseBorrazopolis', 'MunicipiosPR.AnaliseCampinaGrandeDoSul', 'MunicipiosPR.AnaliseCampoDoTenente', 'MunicipiosPR.AnaliseCampoLargo', 'MunicipiosPR.AnaliseCampoMourao', 'MunicipiosPR.AnaliseCascavel', 'MunicipiosPR.AnaliseChopinzinho', 'MunicipiosPR.AnaliseClevelandia', 'MunicipiosPR.AnaliseColorado', 'MunicipiosPR.AnaliseCruzeiroDoOeste', 'MunicipiosPR.AnaliseDoisVizinhos', 'MunicipiosPR.AnaliseDoutorCamargo', 'MunicipiosPR.AnaliseFigueira', 'MunicipiosPR.AnaliseFranciscoBeltrao', 'MunicipiosPR.AnaliseGoioere', 'MunicipiosPR.AnaliseGuaira', 'MunicipiosPR.AnaliseGuaraci', 'MunicipiosPR.AnaliseGuarapuava', 'MunicipiosPR.AnaliseIbaiti', 'MunicipiosPR.AnaliseIbipora', 'MunicipiosPR.AnaliseImbau', 'MunicipiosPR.AnaliseIretama', 'MunicipiosPR.AnaliseItambe', 'MunicipiosPR.AnaliseItapejaraDoeste', 'MunicipiosPR.AnaliseIvaipora', 'MunicipiosPR.AnaliseIzabelDoOeste', 'MunicipiosPR.AnaliseJaniopolis', 'MunicipiosPR.AnaliseJapura', 'MunicipiosPR.AnaliseJardimAlegre', 'MunicipiosPR.AnaliseJoaquimTavora', 'MunicipiosPR.AnaliseJussara', 'MunicipiosPR.AnaliseLapa', 'MunicipiosPR.AnaliseLaranjeirasDoSul', 'MunicipiosPR.AnaliseLondrina', 'MunicipiosPR.AnaliseLuiziana', 'MunicipiosPR.AnaliseLunardelli', 'MunicipiosPR.AnaliseMandaguaçu', 'MunicipiosPR.AnaliseMandaguari', 'MunicipiosPR.AnaliseMandirituba', 'MunicipiosPR.AnaliseMarechalCandidoRondon', 'MunicipiosPR.AnaliseMarilandiaDoSul', 'MunicipiosPR.AnaliseMariluz', 'MunicipiosPR.AnaliseMaringa', 'MunicipiosPR.AnaliseMarquinho', 'MunicipiosPR.AnaliseMatinhos', 'MunicipiosPR.AnaliseNovaLondrina', 'MunicipiosPR.AnaliseNovaOlimpia', 'MunicipiosPR.AnaliseOuroVerdeDoOeste', 'MunicipiosPR.AnaliseParaisoDoNorte', 'MunicipiosPR.AnaliseParanagua', 'MunicipiosPR.AnalisePauloFrontin', 'MunicipiosPR.AnalisePeabiru', 'MunicipiosPR.AnalisePerobal', 'MunicipiosPR.AnalisePiraiDoSul', 'MunicipiosPR.AnalisePontaGrossa', 'MunicipiosPR.AnaliseRibeiraoClaro', 'MunicipiosPR.AnaliseRibeiraoDoPinhal', 'MunicipiosPR.AnaliseRioAzul', 'MunicipiosPR.AnaliseSantaFe', 'MunicipiosPR.AnaliseSantaHelena', 'MunicipiosPR.AnaliseSantaIsabelDoIvai', 'MunicipiosPR.AnaliseSantoAntonioDoSudoeste', 'MunicipiosPR.AnaliseSaoJoaoDoIvai', 'MunicipiosPR.AnaliseSaoJoseDosPinhais', 'MunicipiosPR.AnaliseSaoManoel', 'MunicipiosPR.AnaliseSiqueiraCampos', 'MunicipiosPR.AnaliseTerraBoa', 'MunicipiosPR.AnaliseToledo', 'MunicipiosPR.AnaliseUniaoDaVitoria', 'MunicipiosPR.AnaliseVirmond', 'MunicipiosPR.AnaliseVitorino'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AnaliseCertidoes',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AnaliseCertidoes',
)
