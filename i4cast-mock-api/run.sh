#!/usr/bin/env bash
# -*- coding: utf-8 -*-

gunicorn -c gunicorn.conf.py i4cast_mock_api.app:create_app;
