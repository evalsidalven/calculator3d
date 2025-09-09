import streamlit as st
import pandas as pd

st.set_page_config(page_title="Калькулятор стоимости 3D-печати", layout="wide")
st.title("Калькулятор стоимости 3D-печати")

tab1, tab2 = st.tabs(["FDM", "MSLA"])

with tab1:
    st.header("FDM Калькуляция")
    col1, col2 = st.columns(2)

    with col1:
        printer = st.selectbox("Принтер", ["Bambu Lab P1S", "Другой"],
                               key="fdm_printer")
        material_grams = st.number_input("Материал (г)", min_value=0.0,
                                         value=120.0, key="fdm_grams")
        material_price_per_gram = st.number_input("Цена материала (₽/г)",
                                                  min_value=0.0, value=0.02,
                                                  key="fdm_material_price")
        machine_hours = st.number_input("Машинные часы", min_value=0.0,
                                        value=6.0, key="fdm_machine_hours")
        machine_rate = st.number_input("Ставка за час (₽/ч)", min_value=0.0,
                                       value=600.0, key="fdm_machine_rate")
        operator_hours = st.number_input("Часы оператора", min_value=0.0,
                                         value=0.8, key="fdm_operator_hours")

    with col2:
        operator_rate = st.number_input("Ставка оператора (₽/ч)",
                                        min_value=0.0, value=900.0,
                                        key="fdm_operator_rate")
        postprocessing = st.number_input("Постобработка (₽)", min_value=0.0,
                                         value=500.0, key="fdm_postprocessing")
        consumables = st.number_input("Расходники (₽)", min_value=0.0,
                                      value=100.0, key="fdm_consumables")
        amortization = st.number_input("Амортизация (₽)", min_value=0.0,
                                       value=200.0, key="fdm_amortization")
        margin = st.slider("Маржа (%)", min_value=0, max_value=100, value=25,
                           key="fdm_margin")

    # Расчеты
    material_cost = material_grams * material_price_per_gram
    machine_cost = machine_hours * machine_rate
    operator_cost = operator_hours * operator_rate
    total_cost = material_cost + machine_cost + operator_cost + postprocessing + consumables + amortization
    final_price = total_cost * (1 + margin / 100)
    profit = final_price - total_cost

    # Отображение результатов
    st.subheader("Результаты:")
    col3, col4 = st.columns(2)
    with col3:
        st.metric("Себестоимость (₽)", f"{total_cost:.2f}")
        st.metric("Конечная цена (₽)", f"{final_price:.2f}")
    with col4:
        st.metric("Прибыль (₽)", f"{profit:.2f}")
        st.metric("Зарплата сотрудника (₽)", f"{operator_cost:.2f}")

with tab2:
    st.header("MSLA Калькуляция")
    col1, col2 = st.columns(2)

    with col1:
        resin_volume = st.number_input("Объем смолы (мл)", min_value=0.0,
                                       value=35.0, key="msla_resin")
        resin_price = st.number_input("Цена смолы (₽/мл)", min_value=0.0,
                                      value=2.0, key="msla_resin_price")
        ipa_volume = st.number_input("Изопропил (мл)", min_value=0.0,
                                     value=150.0, key="msla_ipa")
        ipa_price = st.number_input("Цена изопропила (₽/мл)", min_value=0.0,
                                    value=0.3, key="msla_ipa_price")
        gloves = st.number_input("Перчатки (пары)", min_value=0.0, value=0.05,
                                 key="msla_gloves")
        gloves_price = st.number_input("Цена перчаток (₽/пара)", min_value=0.0,
                                       value=20.0, key="msla_gloves_price")

    with col2:
        paper_towels = st.number_input("Бумажные полотенца (листы)",
                                       min_value=0.0, value=2.0,
                                       key="msla_towels")
        towels_price = st.number_input("Цена полотенец (₽/лист)",
                                       min_value=0.0, value=0.5,
                                       key="msla_towels_price")
        cotton_pads = st.number_input("Ватные диски (шт)", min_value=0.0,
                                      value=2.0, key="msla_pads")
        pads_price = st.number_input("Цена дисков (₽/шт)", min_value=0.0,
                                     value=1.0, key="msla_pads_price")
        fep_film = st.number_input("Плёнка FEP (доля)", min_value=0.0,
                                   value=0.01, key="msla_fep")
        fep_price = st.number_input("Цена FEP (₽/шт)", min_value=0.0,
                                    value=1000.0, key="msla_fep_price")
        margin_msla = st.slider("Маржа (%)", min_value=0, max_value=100,
                                value=25, key="msla_margin")

    # Расчет расходников
    resin_cost = resin_volume * resin_price
    ipa_cost = ipa_volume * ipa_price
    gloves_cost = gloves * gloves_price
    towels_cost = paper_towels * towels_price
    pads_cost = cotton_pads * pads_price
    fep_cost = fep_film * fep_price
    total_consumables = resin_cost + ipa_cost + gloves_cost + towels_cost + pads_cost + fep_cost

    # Основные параметры
    print_time = st.number_input("Время печати (ч)", min_value=0.0, value=3.5,
                                 key="msla_print_time")
    machine_rate_msla = st.number_input("Ставка принтера (₽/ч)", min_value=0.0,
                                        value=800.0, key="msla_machine_rate")
    operator_hours_msla = st.number_input("Часы оператора (ч)", min_value=0.0,
                                          value=0.9, key="msla_operator_hours")
    operator_rate_msla = st.number_input("Ставка оператора (₽/ч)",
                                         min_value=0.0, value=900.0,
                                         key="msla_operator_rate")

    # Итоговый расчет
    machine_cost_msla = print_time * machine_rate_msla
    operator_cost_msla = operator_hours_msla * operator_rate_msla
    total_cost_msla = total_consumables + machine_cost_msla + operator_cost_msla
    final_price_msla = total_cost_msla * (1 + margin_msla / 100)
    profit_msla = final_price_msla - total_cost_msla

    # Отображение результатов
    st.subheader("Результаты:")
    col3, col4 = st.columns(2)
    with col3:
        st.metric("Общая стоимость расходников (₽)",
                  f"{total_consumables:.2f}")
        st.metric("Себестоимость (₽)", f"{total_cost_msla:.2f}")
    with col4:
        st.metric("Конечная цена (₽)", f"{final_price_msla:.2f}")
        st.metric("Прибыль (₽)", f"{profit_msla:.2f}")