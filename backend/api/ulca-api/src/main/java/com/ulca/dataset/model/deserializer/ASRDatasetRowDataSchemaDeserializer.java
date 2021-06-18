package com.ulca.dataset.model.deserializer;

import java.io.IOException;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import org.json.JSONObject;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.deser.std.StdDeserializer;

import io.swagger.model.ASRParamsSchema;
import io.swagger.model.ASRParamsSchema.AgeEnum;
import io.swagger.model.ASRParamsSchema.DialectEnum;
import io.swagger.model.ASRRowSchema;
import io.swagger.model.AudioBitsPerSample;
import io.swagger.model.AudioChannel;
import io.swagger.model.AudioFormat;
import io.swagger.model.AudioQualityEvaluation;
import io.swagger.model.AudioQualityEvaluation.MethodTypeEnum;
import io.swagger.model.CollectionDetailsAudioAutoAligned;
import io.swagger.model.CollectionDetailsMachineGeneratedTranscript;
import io.swagger.model.CollectionDetailsManualTranscribed;
import io.swagger.model.CollectionMethodAudio;
import io.swagger.model.DatasetType;
import io.swagger.model.Domain;
import io.swagger.model.DomainEnum;
import io.swagger.model.Gender;
import io.swagger.model.LanguagePair;
import io.swagger.model.Source;
import io.swagger.model.Submitter;
import io.swagger.model.TranscriptionEvaluationMethod1;
import io.swagger.model.WadaSnr;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class ASRDatasetRowDataSchemaDeserializer extends StdDeserializer<ASRRowSchema> {

	protected ASRDatasetRowDataSchemaDeserializer(Class<?> vc) {
		super(vc);
		// TODO Auto-generated constructor stub
	}

	public ASRDatasetRowDataSchemaDeserializer() {
		this(null);
		// TODO Auto-generated constructor stub
	}

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	@Override
	public ASRRowSchema deserialize(JsonParser p, DeserializationContext ctxt)
			throws IOException, JsonProcessingException {

		log.info("******** inside deserializer ********");
		ObjectMapper mapper = new ObjectMapper();
		ASRRowSchema asrRowSchema = new ASRRowSchema();
		JsonNode node = p.readValueAsTree();

		ArrayList<String> errorList = new ArrayList<String>();

		JSONObject obj = new JSONObject(node.toPrettyString());

		Set<String> keys = obj.keySet();

		for (String k : keys) {
			try {
				AsrRowDataSchemaKeys key = AsrRowDataSchemaKeys.valueOf(k);
			} catch (Exception ex) {
				log.info("AsrRowDataSchemaKeys not valid ");
				errorList.add(k + " unknown property ");
			}

		}
		// required

		if (!node.has("audioFilename")) {
			errorList.add("audioFilename field should be present");
		} else if (!node.get("audioFilename").isTextual()) {
			errorList.add("audioFilename field should be String");
		} else {

			String audioFilename = node.get("audioFilename").asText();
			asrRowSchema.setAudioFilename(audioFilename);

		}

		if (!node.has("text")) {
			errorList.add("text field should be present");
		} else if (!node.get("text").isTextual()) {
			errorList.add("text field should be String");
		} else {

			String text = node.get("text").asText();
			asrRowSchema.setText(text);

		}

		if (!node.has("endTime")) {
			errorList.add("endTime field should be present");
		} else if (!node.get("endTime").isTextual()) {
			errorList.add("endTime field should be String");
		} else {
			String endTime = node.get("endTime").asText();
			asrRowSchema.setEndTime(endTime);
		}

		// optional params

		if (node.has("startTime")) {
			if (!node.get("startTime").isTextual()) {
				errorList.add("startTime field should be String");
			} else {

				String startTime = node.get("startTime").asText();
				asrRowSchema.setStartTime(startTime);

			}
		}

		if (node.has("channel")) {
			if (!node.get("channel").isTextual()) {
				errorList.add("channel field should be String");
			} else {
				String channel = node.get("channel").asText();
				AudioChannel audioChannel = AudioChannel.fromValue(channel);
				if (audioChannel != null) {
					asrRowSchema.setChannel(audioChannel);
				} else {
					errorList.add("channel not among one of specified");
				}

			}

		}

		if (node.has("samplingRate")) {
			if (!node.get("samplingRate").isNumber()) {
				errorList.add("samplingRate field should be Number");
			} else {
				BigDecimal samplingRate = node.get("samplingRate").decimalValue();
				asrRowSchema.setSamplingRate(samplingRate);

			}

		}

		if (node.has("bitsPerSample")) {
			if (!node.get("bitsPerSample").isTextual()) {
				errorList.add("bitsPerSample field should be String");
			} else {
				String bitsPerSample = node.get("bitsPerSample").asText();

				AudioBitsPerSample audioBitsPerSample = AudioBitsPerSample.fromValue(bitsPerSample);
				if (audioBitsPerSample != null) {
					asrRowSchema.setBitsPerSample(audioBitsPerSample);

				} else {
					errorList.add("bitsPerSample not among one of specified");
				}

			}

		}

		if (node.has("gender")) {
			if (!node.get("gender").isTextual()) {
				errorList.add("gender field should be String");
			} else {
				String gender = node.get("gender").asText();

				Gender genderenum = Gender.fromValue(gender);

				if (genderenum != null) {
					asrRowSchema.setGender(genderenum);

				} else {
					errorList.add("gender not among one of specified values");
				}
			}
		}

		if (node.has("age")) {
			if (!node.get("age").isTextual()) {
				errorList.add("age field should be String");
			} else {
				String age = node.get("age").asText();

				ASRRowSchema.AgeEnum ageEnum = ASRRowSchema.AgeEnum.fromValue(age);

				if (ageEnum != null) {
					asrRowSchema.setAge(ageEnum);

				} else {
					errorList.add("age not among one of specified values");
				}
			}
		}
		if (node.has("dialect")) {
			if (!node.get("dialect").isTextual()) {
				errorList.add("dialect field should be String");
			} else {
				String dialect = node.get("dialect").asText();
				ASRRowSchema.DialectEnum dialectEnum = ASRRowSchema.DialectEnum.fromValue(dialect);

				if (dialectEnum != null) {
					asrRowSchema.setDialect(dialectEnum);

				} else {
					errorList.add("dialect not among one of specified values");
				}
			}
		}

		if (node.has("snr")) {
			if (!node.get("snr").has("methodType")) {
				errorList.add("methodType should be present");
			} else if (!node.get("snr").get("methodType").isTextual()) {
				errorList.add("methodType should be String");
			} else {
				String methodType = node.get("snr").get("methodType").asText();
				if (methodType.equals("WadaSnr")) {
					WadaSnr wadaSnr = mapper.readValue(node.get("snr").get("methodDetails").toPrettyString(),
							WadaSnr.class);
					AudioQualityEvaluation audioQualityEvaluation = new AudioQualityEvaluation();
					audioQualityEvaluation.setMethodType(MethodTypeEnum.WADASNR);
					audioQualityEvaluation.setMethodDetails(wadaSnr);
					asrRowSchema.setSnr(audioQualityEvaluation);

				} else {
					errorList.add("methodType is not one of specified values");
				}

			}

		}

		if (node.has("collectionMethod")) {
			if (node.get("collectionMethod").has("collectionDescription")) {
				if (!node.get("collectionMethod").get("collectionDescription").isArray()) {
					errorList.add("collectionDescription field should be String Array");
				} else {

					try {
						String collectionDescription = node.get("collectionMethod").get("collectionDescription").get(0)
								.asText();
						CollectionMethodAudio.CollectionDescriptionEnum collectionDescriptionEnum = CollectionMethodAudio.CollectionDescriptionEnum
								.fromValue(collectionDescription);

						CollectionMethodAudio collectionMethodAudio = new CollectionMethodAudio();
						List<CollectionMethodAudio.CollectionDescriptionEnum> list = new ArrayList<CollectionMethodAudio.CollectionDescriptionEnum>();
						list.add(collectionDescriptionEnum);
						collectionMethodAudio.setCollectionDescription(list);

						switch (collectionDescriptionEnum) {
						case AUTO_ALIGNED:
							if (node.get("collectionMethod").get("collectionDetails").has("alignmentTool")) {
								if (!node.get("collectionMethod").get("collectionDetails").get("alignmentTool")
										.isTextual()) {
									String alignmentTool = node.get("collectionMethod").get("collectionDetails")
											.get("alignmentTool").asText();
									CollectionDetailsAudioAutoAligned.AlignmentToolEnum alignmentToolEnum = CollectionDetailsAudioAutoAligned.AlignmentToolEnum
											.fromValue(alignmentTool);
									if (alignmentToolEnum != null) {

										CollectionDetailsAudioAutoAligned collectionDetailsAudioAutoAligned = mapper
												.readValue(
														node.get("collectionMethod").get("collectionDetails")
																.toPrettyString(),
														CollectionDetailsAudioAutoAligned.class);

										collectionMethodAudio.setCollectionDetails(collectionDetailsAudioAutoAligned);
										asrRowSchema.setCollectionMethod(collectionMethodAudio);

									} else {
										errorList.add("alignmentTool should be from one of specified values");
									}

								} else {
									errorList.add("alignmentTool should be String");
								}

							} else {
								errorList.add("alignmentTool should be present");
							}

							break;

						case MACHINE_GENERATED_TRANSCRIPT:

							CollectionDetailsMachineGeneratedTranscript collectionDetailsMachineGeneratedTranscript = new CollectionDetailsMachineGeneratedTranscript();
							TranscriptionEvaluationMethod1 transcriptionEvaluationMethod1 = mapper
									.readValue(
											node.get("collectionMethod").get("collectionDetails")
													.get("evaluationMethod").toPrettyString(),
											TranscriptionEvaluationMethod1.class);

							collectionDetailsMachineGeneratedTranscript
									.setEvaluationMethod(transcriptionEvaluationMethod1);

							collectionDetailsMachineGeneratedTranscript.setAsrModel(
									node.get("collectionMethod").get("collectionDetails").get("asrModel").asText());
							collectionMethodAudio.setCollectionDetails(collectionDetailsMachineGeneratedTranscript);

							String evaluationMethodType = node.get("collectionMethod").get("collectionDetails")
									.get("evaluationMethodType").asText();

							CollectionDetailsMachineGeneratedTranscript.EvaluationMethodTypeEnum evaluationMethodTypeEnum = CollectionDetailsMachineGeneratedTranscript.EvaluationMethodTypeEnum
									.fromValue(evaluationMethodType);
							collectionDetailsMachineGeneratedTranscript
									.setEvaluationMethodType(evaluationMethodTypeEnum);

							collectionDetailsMachineGeneratedTranscript.setAsrModelVersion(node.get("collectionMethod")
									.get("collectionDetails").get("asrModelVersion").asText());

							asrRowSchema.setCollectionMethod(collectionMethodAudio);

							log.info("machine-generated-transcript");

							break;

						case MANUAL_TRANSCRIBED:

							CollectionDetailsManualTranscribed collectionDetailsManualTranscribed = mapper.readValue(
									node.get("collectionMethod").get("collectionDetails").toPrettyString(),
									CollectionDetailsManualTranscribed.class);
							collectionMethodAudio.setCollectionDetails(collectionDetailsManualTranscribed);
							asrRowSchema.setCollectionMethod(collectionMethodAudio);

							log.info("manual-transcribed");

							break;

						}

					} catch (Exception e) {
						System.out.println("collection method not proper");
						errorList.add("collectionMethod field value not proper.");
						System.out.println("tracing the error");

						e.printStackTrace();
					}

				}
			}
		}

		if (!errorList.isEmpty())
			throw new IOException(errorList.toString());

		log.info("******** Exiting deserializer ********");
		return asrRowSchema;
	}

}
