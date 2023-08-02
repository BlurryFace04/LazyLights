const axios = require('axios');
const {
  SinricPro, startSinricPro
} = require('sinricpro');

const appKey = '1433ab95-e75a-42fd-992b-65004223fef7';
const device1 = '64c9220635be2dbc3edd46d7';
const device2 = '64c9225335be2dbc3edd4765';
const secretKey = '69932de1-e937-4d7b-9c48-dfe025427d50-94f3e47e-62ac-4cf6-887e-1d3380b956b6';
const deviceIds = [device1, device2];

const send_command_to_device = async (appliance_name) => {
  const url = 'http://192.168.91.53:5069/jsonex';
  const data = {
    appliance: appliance_name
  };
  await axios.post(url, data, { headers: { 'Content-Type': 'application/json' } });
};

const setPowerState = async (deviceId, data) => {
  if (deviceId === device1) {
    await send_command_to_device('tl');
  } else if (deviceId === device2) {
    await send_command_to_device('bl');
  }
  return true;
};

const sinricpro = new SinricPro(appKey, deviceIds, secretKey, true);
const callbacks = { setPowerState };

startSinricPro(sinricpro, callbacks);