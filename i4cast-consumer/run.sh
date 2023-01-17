#!/usr/bin/env bash
# -*- coding: utf-8 -*-

STATION=$1;
ENVIRONMENTAL_TYPE=$2;

validate_station_parameter() {
    if [ -z ${STATION} ]; then
        echo 'Parâmetro `STATION` não informado!';
        exit -1;
    fi;
}

validate_env_type_parameter() {
    if [ -z ${ENVIRONMENTAL_TYPE} ]; then
        echo 'Parâmetro `ENVIRONMENTAL_TYPE` não informado!';
        exit -1;
    fi;
}

validate_parameters() {
    validate_station_parameter;
    validate_env_type_parameter;
}

run_i4cast_consumer() {
    python -m i4cast_consumer --station ${STATION} --environmental_type ${ENVIRONMENTAL_TYPE};
}

compress_output_files() {
    echo '';
    echo 'Compactando arquivos gerados...'

    NOW=$(date +'%s');
    tar -czvf output-${NOW}.tar.gz ./dist/*;
}

main() {
    validate_parameters;
    run_i4cast_consumer;

    if [ $? -eq 0 ]; then
        compress_output_files;
    
    else
        echo 'Houve um erro ao executar o procedimento.';
    fi
}

main;
