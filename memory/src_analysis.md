# ApolloDocs `src` Directory Analysis

The `src` directory functions as the central "engine" or domain layer of ApolloDocs. It handles the core engineering calculations and document generation independent of web framework specifics (FastAPI) or database interactions (SQLAlchemy). 

All traffic to and from the API is translated into pure Python Data Transfer Objects (DTOs) and Domain logic here to output the required engineering files (Memorial Descritivo, Diagrama Unifilar, Formulários ENEL, Procurações).

---

## Architecture Overview

The `src` module follows a Clean Architecture approach:
1. **Inputs:** Pydantic models from the API are processed via Factory classes.
2. **Domain/Calculations:** Pure business and engineering logic is applied within domain objects.
3. **Data Schemas:** Standardized Python DataClasses map inputs, processes, and outputs reliably.
4. **Document Builders:** Specialized builder scripts take the final compiled DataClasses and generate PDFs via templating (HTML/Jinja -> WeasyPrint) or raw PDF manipulation (PyMuPDF).

## Directory Structure & Key Files

### Root `src/` Files
* `config.py`: The single source of truth for engineering constants (e.g., base voltage drops `RESISTIVIDADE_COBRE`, Ceará regional irradiance factors `HORAS_SOL_PLENO_MEDIA_CE`) and absolute paths to template files ensuring portability.
* `createproject.py`: Contains `ProjectFactory` and `SistemaInstaladoFactory`. Its job is to ingest raw dictionary/JSON or API layer representations (`ProjetoMemorial`) and instantiate typed Domain `dataclasses` (`ProjetoCompleto`, `ConfiguracaoSistema`).

### `src/schemas/`
Houses pure Python `dataclasses` ensuring type safety across the `src` domain, decoupling it entirely from FastAPI models.
* `modelreturnobject.py`: Extremely crucial file declaring DTOs like `RetornoProjetoCompleto` (aggregates everything a Memorial requires), `RetornoProjetoDiagrama`, and definitions for `ConfiguracaoSistema`, `Inversor`, `Placa`.
* `models.py` / `constantes.py`: Stores constants, ENUMs and reusable literal types (monofásico, trifásico, etc.).

### `src/domain/`
The brain doing all necessary solar calculation, formatting equations, and mapping strings.
* `creatediagramobject.py` (`ObjetoDiagramaUnifilar`): Prepares and performs validations specific for diagrams (e.g., calculates wire sizing text, breaker specs, strings placement based on single/dual/triple inverter setups).
* `creatememorialobject.py` (`ObjetosCalculados`): Handles deep Math operations. Calculates load demands, voltage drops, maximum and effectively calculated solar power, string distributions on MPPTs, strings formatted for the `.html` templates, etc. Returns fully saturated `RetornoProjetoCompleto`.
* `utils/calculos.py`: Core utility functions isolating the pure math equations (amps to breaker rules, wire dimension tables).
* `texts/`: Fixed blocks of domain texts mapped to be injected into the generated PDFs.

### `src/buildingdocuments/`
This layer is responsible for the actual "paint to canvas". It takes output from `src/domain/` objects.
* `memorialdescritivo.py`: Uses `weasyprint` and `matplotlib` (for turning LaTeX into `base64` PNG equations!) built over `Jinja2` `HTML` templates. Returns raw PDF bytes.
* `unifilar.py`: Uses `PyMuPDF` (`fitz`) to read base PDF diagram templates from `support-files/templates_diagramaunifilar/` and manually draws lines (for breakers/wires) and text at absolute coordinates `(x, y)` to build single-line diagrams.
* `formularioENEL.py` & `procuracao.py`: Tools for other standard engineering forms.

### `src/templates/`
Contains raw `.html` files (`memorial.html`, `procuracao.html`) infused with Jinja logic (`{{ dados.nome_cliente }}`) that provide the styling shell for WeasyPrint to transform into beautiful PDFs.

---

## Agent Guide: Editing this Engine

If you are an agent tasked with updating logic or adding features to this core, adhere strictly to these rules:

1. **Maintain Decoupling:** NEVER import `SQLAlchemy` queries, `FastAPI` context, or HTTP Request objects directly into `src/`. If a new parameter from the user is needed, it must first be added to the input Pydantic model (`api/schemas/`), then mapped in `src/createproject.py` or passed into the DTO in `schemas/modelreturnobject.py`.
2. **Follow the Pipeline:** Feature execution should follow this sequence:
   * **1.** Update `dataclasses` in `src/schemas/modelreturnobject.py` to support new variables.
   * **2.** Map the new incoming variables in `src/createproject.py`.
   * **3.** Create the calculus function in `src/domain/utils/calculos.py`.
   * **4.** Wire the calculus function into the specific return Object in `src/domain/creatememorialobject.py` or `creatediagramobject.py`.
   * **5.** Modify the Template engine `src/buildingdocuments/` and the UI source files in `src/templates/`.
3. **Template Paths & Engineering Values:** Use `config.py` for ANY constants. Do not hardcode new constants like wire limits scattered in the math logics.
4. **Drawing Diagrams:** When editing `unifilar.py`, remember it relies on absolute coordinate strings on standard templates. Any new components will require manual placement `(page.insert_text((x, y), ...))` or lines arrays `(page.draw_line(p1, p2))`. If the user asks you to modify diagram logic, view the existing offsets rigorously.
5. **PDF Rendering & Equations:** `creatememorialobject.py` generates LaTeX strings (`equation4 = r"$\Delta V...$"`). `memorialdescritivo.py` uses Matplotlib to silently convert these to images. Do NOT feed unescaped special characters directly as they will break Matplotlib's `ax.text` LaTeX renderer. Always use raw strings (`r""`) for math logic.
