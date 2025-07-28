var hls;
		var heartbeatlive = null;

			function enableHlsHeartbeatLive(media, videoElement, hlsPlayer) {
				function playerHls(hlsPlayer) {
					var self = this;
					self.hls = hlsPlayer
					this.getCurrentVideoBitrate = function () {
						if (self.hls.levels && self.hls.loadLevel >= 0)
							return Math.round(self.hls.levels[self.hls.loadLevel].bitrate / 1000);

						return 0;
					}
				}
				if (!heartbeatlive) {
					var pplayer = new playerHls(hlsPlayer);
					heartbeatlive = new HeartbeatLive(media.userId, media.profileId, media.liveEventId, media.liveDateTimeId, media.liveGridId, media.liveGridProgramId);
					heartbeatlive.attachPlayer(videoElement, pplayer);
				}
			}


		var video = document.getElementById('player-live');
		var media = {
			userId: 18733037,
			profileId: "b01aae7e-e23f-415f-a71b-dba33b1bebc2",
			liveEventId: 191,
			liveDateTimeId: 1295,
			liveGridId: 3061,
			liveGridProgramId: 244
												};

		var heartbeatEnable = false;

		function appsFlyer(eventName, eventValue) {
			AF('pba', 'event', {
				eventName: eventName,
				eventValue: { eventValue }
			});
		}

		function initLive(urlHLS, urlHLSBackup, sourceVideo) {
			var isFirstPlay = true;
			if (Hls.isSupported()) {
				if (hls) { hls.destroy(); }
				hls = new Hls({
					cmcd: true,
					enableWorker: true,
					abrBandWidthFactor: 0.8,
					abrBandWidthUpFactor: 0.7,
					maxBufferLength: 20
				});
				hls.loadSource(sourceVideo == 0 ? urlHLS : urlHLSBackup);
				hls.attachMedia(video);
				hls.on(Hls.Events.MANIFEST_LOADED, function () {
					if (!heartbeatEnable) {
						enableHlsHeartbeatLive(media, video, hls);
						heartbeatEnable = true;
					}
					checkSubTitle();
					hls.on(window.Hls.Events.ERROR, (event, { details }) => {
						if (details === window.Hls.ErrorDetails.BUFFER_STALLED_ERROR) {
							$('.loader-player').show();
						}
					})

					hls.on(window.Hls.Events.FRAG_BUFFERED, () => {
						$('.playerVersion').show();
						$('.loader-player').hide();
						if (isFirstPlay) {
							video.play();
							isFirstPlay = false;
						}
					})
				});

				hls.on(Hls.Events.ERROR, function (name, data) {
					switch (data.details) {
						case Hls.ErrorDetails.MANIFEST_LOAD_TIMEOUT:
						case Hls.ErrorDetails.MANIFEST_LOAD_ERROR:
						case Hls.ErrorDetails.MANIFEST_PARSING_ERROR:
						case "levelLoadError":
							var timeWait = 5000 * sourceVideo;
							if (sourceVideo == 0) sourceVideo = 1;
							else sourceVideo = 0;

							setTimeout(function () {
								initLive(urlHLS, urlHLSBackup, sourceVideo)
							}, timeWait);
							break;
					}
				});
			} else if (video.canPlayType('application/vnd.apple.mpegurl')) {
				video.src = 'https://brasil.cdnsimba.com.br/bpk-tv/RecordNEWS/default/index.m3u8?auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmkiOiIvYnBrLXR2L1JlY29yZE5FV1MvZGVmYXVsdC9pbmRleC5tM3U4IiwibWV0aG9kIjoiR0VUIiwiZXhwIjoxNzUzNDI2Nzg1fQ.3HFBRs56g3sqaXIi-jvuM5pUONFFRgoEBXMi-TGFRgU';
				video.addEventListener('loadedmetadata', function () {
					video.play();
					$('.loader-player').hide()
				});
			}

		}

		var urlLive = 'https://brasil.cdnsimba.com.br/bpk-tv/RecordNEWS/default/index.m3u8?auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmkiOiIvYnBrLXR2L1JlY29yZE5FV1MvZGVmYXVsdC9pbmRleC5tM3U4IiwibWV0aG9kIjoiR0VUIiwiZXhwIjoxNzUzNDI2Nzg1fQ.3HFBRs56g3sqaXIi-jvuM5pUONFFRgoEBXMi-TGFRgU';
		var urlLiveBackup = 'https://brasil.cdnsimba.com.br/bpk-tv/RecordNEWS/default/index.m3u8?auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmkiOiIvYnBrLXR2L1JlY29yZE5FV1MvZGVmYXVsdC9pbmRleC5tM3U4IiwibWV0aG9kIjoiR0VUIiwiZXhwIjoxNzUzNDI2Nzg1fQ.3HFBRs56g3sqaXIi-jvuM5pUONFFRgoEBXMi-TGFRgU';
