const axios = require('axios');
const {
  SinricPro, startSinricPro
} = require('sinricpro');

const appKey = 'API-KEY';
const device1 = 'DEVICE1-ID';
const device2 = 'DEVICE2-ID';
const device3 = 'DEVICE3-ID';
const device4 = 'DEVICE4-ID';
const secretKey = 'SECRET-KEY';
const deviceIds = [device1, device2, device3, device4];

const send_command_to_device = async (appliance_name) => {
  const url = 'http://192.168.1.3:5069/jsonex';
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
  } else if (deviceId === device3) {
    await send_command_to_device('f');
  } else if (deviceId === device4) {
    await send_command_to_device('s');
  }
  return true;
};

const sinricpro = new SinricPro(appKey, deviceIds, secretKey, true);
const callbacks = { setPowerState };

startSinricPro(sinricpro, callbacks);
