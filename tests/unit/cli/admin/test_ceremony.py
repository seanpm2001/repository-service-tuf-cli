from unittest.mock import MagicMock

import pretend  # type: ignore
from securesystemslib.keys import generate_ed25519_key  # type: ignore

from kaprien.cli.admin.ceremony import ceremony


class TestCeremonyGroupCLI:
    def test_ceremony(self, client, test_context):
        test_result = client.invoke(ceremony, obj=test_context)
        assert test_result.exit_code == 1
        assert (
            "Repository Metadata and Settings for Kaprien"
            in test_result.output
        )

    def test_ceremony_start_no(self, client, test_context):
        test_result = client.invoke(ceremony, input="n\nn\n", obj=test_context)
        assert "Ceremony aborted." in test_result.output
        assert test_result.exit_code == 1

    def test_ceremony_start_not_ready_load_the_keys(
        self, client, test_context
    ):
        input_step1 = [
            "n",
            "y",
            "",
            "",
            "",
            "",
            "",
            "",
            "y",
            "http://www.example.com/repository",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        input_step2 = ["n"]
        test_result = client.invoke(
            ceremony,
            input="\n".join(input_step1 + input_step2),
            obj=test_context,
        )
        assert "Ceremony aborted." in test_result.output
        assert test_result.exit_code == 1

    def test_ceremony_start_default_values(
        self, client, monkeypatch, test_context
    ):
        input_step1 = [
            "y",
            "y",
            "",
            "",
            "",
            "",
            "",
            "",
            "y",
            "https://github.com/KAPRIEN",
            "*, */*, */*/*, */*/*/*, */*/*/*/*, */*/*/*/*/*",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "4",
            "",
        ]
        input_step2 = [
            "Y",
            "tests/files/JimiHendrix.key",
            "strongPass",
            "tests/files/JanisJoplin.key",
            "strongPass",
            "tests/files/ChrisCornel.key",
            "strongPass",
            "tests/files/KurtCobain.key",
            "strongPass",
            "tests/files/snapshot1.key",
            "strongPass",
            "tests/files/timestamp1.key",
            "strongPass",
            "tests/files/JoeCocker.key",
            "strongPass",
            "tests/files/bins1.key",
            "strongPass",
            "y",
            "y",
            "y",
            "y",
            "y",
            "y",
        ]

        class FakeKey:
            def __init__(self):
                self.error = None
                self.key = generate_ed25519_key()

        fake__load_key = pretend.call_recorder(lambda *a, **kw: FakeKey())
        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony._load_key", fake__load_key
        )

        test_result = client.invoke(
            ceremony,
            input="\n".join(input_step1 + input_step2),
            obj=test_context,
        )

        assert test_result.exit_code == 0
        assert "Role: root" in test_result.output
        assert "Number of Keys: 1" in test_result.output
        assert "Threshold: 1" in test_result.output
        assert "Keys Type: offline" in test_result.output
        assert "JimiHendrix.key" in test_result.output
        assert "Role: targets" in test_result.output
        assert "Number of Keys: 1" in test_result.output
        assert "JanisJoplin.key" in test_result.output
        assert "ChrisCornel.key" in test_result.output
        assert "Role: snapshot" in test_result.output
        assert "Keys Type: online" in test_result.output
        assert "Role: timestamp" in test_result.output
        assert "KurtCobain.key" in test_result.output
        assert "JoeCocker.key" in test_result.output
        assert "bins1.key" in test_result.output
        # passwords not shown in output
        assert "strongPass" not in test_result.output

    def test_ceremony_start_default_values_reconfigure_one_role(
        self, client, monkeypatch, test_context
    ):
        input_step1 = [
            "y",
            "y",
            "",
            "",
            "",
            "",
            "",
            "",
            "y",
            "http://www.example.com/repository",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        input_step2 = [
            "Y",
            "tests/files/JimiHendrix.key",
            "strongPass",
            "tests/files/JanisJoplin.key",
            "strongPass",
            "tests/files/ChrisCornel.key",
            "strongPass",
            "tests/files/KurtCobain.key",
            "strongPass",
            "tests/files/snapshot1.key",
            "strongPass",
            "tests/files/timestamp1.key",
            "strongPass",
            "tests/files/JoeCocker.key",
            "strongPass",
            "tests/files/bins1.key",
            "strongPass",
            "y",
            "y",
            "n",
            "",
            "",
            "",
            "tests/files/snapshot1.key",
            "strongPass",
            "y",
            "y",
            "y",
            "y",
        ]

        class FakeKey:
            def __init__(self):
                self.error = None
                self.key = generate_ed25519_key()

        fake__load_key = pretend.call_recorder(lambda *a, **kw: FakeKey())
        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony._load_key", fake__load_key
        )

        test_result = client.invoke(
            ceremony,
            input="\n".join(input_step1 + input_step2),
            obj=test_context,
        )
        assert test_result.exit_code == 0
        assert "Role: root" in test_result.output
        assert "Number of Keys: 1" in test_result.output
        assert "Threshold: 1" in test_result.output
        assert "Keys Type: offline" in test_result.output
        assert "JimiHendrix.key" in test_result.output
        assert "Role: targets" in test_result.output
        assert "Number of Keys: 1" in test_result.output
        assert "JanisJoplin.key" in test_result.output
        assert "ChrisCornel.key" in test_result.output
        assert "Role: snapshot" in test_result.output
        assert "Keys Type: online" in test_result.output
        assert "Role: timestamp" in test_result.output
        assert "KurtCobain.key" in test_result.output
        assert "JoeCocker.key" in test_result.output
        assert "bins1.key" in test_result.output
        # passwords not shown in output
        assert "strongPass" not in test_result.output

    def test_ceremony_with_flag_bootstrap(
        self, client, monkeypatch, test_context
    ):
        input_step1 = [
            "y",
            "y",
            "",
            "",
            "",
            "",
            "",
            "",
            "y",
            "http://www.example.com/repository",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        input_step2 = [
            "Y",
            "tests/files/JimiHendrix.key",
            "strongPass",
            "tests/files/JanisJoplin.key",
            "strongPass",
            "tests/files/ChrisCornel.key",
            "strongPass",
            "tests/files/KurtCobain.key",
            "strongPass",
            "tests/files/snapshot1.key",
            "strongPass",
            "tests/files/timestamp1.key",
            "strongPass",
            "tests/files/JoeCocker.key",
            "strongPass",
            "tests/files/bins1.key",
            "strongPass",
            "y",
            "y",
            "y",
            "y",
            "y",
            "y",
        ]

        mocked_check_server = pretend.call_recorder(
            lambda s: {"Authorization": "Bearer test"}
        )
        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony._check_server", mocked_check_server
        )

        fake_response_get = pretend.stub(
            status_code=200,
            json=pretend.call_recorder(lambda: {"boostrap": False}),
        )
        fake_response_post = pretend.stub(
            status_code=202,
            json=pretend.call_recorder(
                lambda: {"message": "Bootstrap accepted."}
            ),
        )
        mocked_request_server = MagicMock()
        mocked_request_server.side_effect = [
            fake_response_get,
            fake_response_post,
        ]

        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony.request_server",
            mocked_request_server,
        )

        class FakeKey:
            def __init__(self):
                self.error = None
                self.key = generate_ed25519_key()

        fake__load_key = pretend.call_recorder(lambda *a, **kw: FakeKey())
        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony._load_key", fake__load_key
        )

        # simulate the settings file
        test_context["settings"].SERVER = "fake-server"
        test_context["settings"].TOKEN = "test-token"
        # write settings
        test_result = client.invoke(
            ceremony,
            ["--bootstrap"],
            input="\n".join(input_step1 + input_step2),
            obj=test_context,
        )

        assert test_result.exit_code == 0
        assert "Ceremony and Bootstrap done" in test_result.output
        # passwords not shown in output
        assert "strongPass" not in test_result.output

    def test_ceremony_with_flag_bootstrap_already_done(
        self, client, monkeypatch, test_context
    ):
        mocked_check_server = pretend.call_recorder(
            lambda s: {"Authorization": "Bearer test"}
        )
        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony._check_server", mocked_check_server
        )

        mocked_request_server = pretend.stub(
            status_code=200,
            json=pretend.call_recorder(
                lambda: {
                    "bootstrap": True,
                    "message": "System already has a Metadata.",
                }
            ),
        )

        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony.request_server",
            lambda *a, **kw: mocked_request_server,
        )

        # simulate the settings file
        test_context["settings"].SERVER = "fake-server"
        test_context["settings"].TOKEN = "test-token"

        test_result = client.invoke(
            ceremony, ["--bootstrap"], obj=test_context
        )

        assert test_result.exit_code == 1
        assert "System already has a Metadata." in test_result.output

    def test_ceremony_with_flag_bootstrap_forbidden(
        self, client, monkeypatch, test_context
    ):
        mocked_check_server = pretend.call_recorder(
            lambda s: {"Authorization": "Bearer test"}
        )
        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony._check_server", mocked_check_server
        )

        mocked_request_server = pretend.stub(
            status_code=401,
            json=pretend.call_recorder(
                lambda: {
                    "detail": "Unauthorized.",
                }
            ),
        )

        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony.request_server",
            lambda *a, **kw: mocked_request_server,
        )

        # simulate the settings file
        test_context["settings"].SERVER = "fake-server"
        test_context["settings"].TOKEN = "test-token"

        test_result = client.invoke(
            ceremony, ["--bootstrap"], obj=test_context
        )

        assert test_result.exit_code == 1
        assert "Error 401 Unauthorized." in test_result.output

    def test_ceremony_with_flag_bootstrap_failed_post(
        self, client, monkeypatch, test_context
    ):
        input_step1 = [
            "y",
            "y",
            "",
            "",
            "",
            "",
            "",
            "",
            "y",
            "http://www.example.com/repository",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        input_step2 = [
            "Y",
            "tests/files/JimiHendrix.key",
            "strongPass",
            "tests/files/JanisJoplin.key",
            "strongPass",
            "tests/files/ChrisCornel.key",
            "strongPass",
            "tests/files/KurtCobain.key",
            "strongPass",
            "tests/files/snapshot1.key",
            "strongPass",
            "tests/files/timestamp1.key",
            "strongPass",
            "tests/files/JoeCocker.key",
            "strongPass",
            "tests/files/bins1.key",
            "strongPass",
            "y",
            "y",
            "y",
            "y",
            "y",
            "y",
        ]

        mocked_check_server = pretend.call_recorder(
            lambda s: {"Authorization": "Bearer test"}
        )
        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony._check_server", mocked_check_server
        )

        fake_response_get = pretend.stub(
            status_code=200,
            json=pretend.call_recorder(lambda: {"boostrap": False}),
        )
        fake_response_post = pretend.stub(
            status_code=403,
            json=pretend.call_recorder(lambda: {"detail": "Forbidden"}),
        )
        mocked_request_server = MagicMock()
        mocked_request_server.side_effect = [
            fake_response_get,
            fake_response_post,
        ]

        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony.request_server",
            mocked_request_server,
        )

        class FakeKey:
            def __init__(self):
                self.error = None
                self.key = generate_ed25519_key()

        fake__load_key = pretend.call_recorder(lambda *a, **kw: FakeKey())
        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony._load_key", fake__load_key
        )

        # simulate the settings file
        test_context["settings"].SERVER = "fake-server"
        test_context["settings"].TOKEN = "test-token"
        # write settings
        test_result = client.invoke(
            ceremony,
            ["--bootstrap"],
            input="\n".join(input_step1 + input_step2),
            obj=test_context,
        )

        assert test_result.exit_code == 1
        assert "Error 403 Forbidden" in test_result.output

    def test_ceremony_with_flag_bootstrap_unexpected_error(
        self, client, monkeypatch, test_context
    ):
        input_step1 = [
            "y",
            "y",
            "",
            "",
            "",
            "",
            "",
            "",
            "y",
            "http://www.example.com/repository",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
        input_step2 = [
            "Y",
            "tests/files/JimiHendrix.key",
            "strongPass",
            "tests/files/JanisJoplin.key",
            "strongPass",
            "tests/files/ChrisCornel.key",
            "strongPass",
            "tests/files/KurtCobain.key",
            "strongPass",
            "tests/files/snapshot1.key",
            "strongPass",
            "tests/files/timestamp1.key",
            "strongPass",
            "tests/files/JoeCocker.key",
            "strongPass",
            "tests/files/bins1.key",
            "strongPass",
            "y",
            "y",
            "y",
            "y",
            "y",
            "y",
        ]

        mocked_check_server = pretend.call_recorder(
            lambda s: {"Authorization": "Bearer test"}
        )
        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony._check_server", mocked_check_server
        )

        fake_response_get = pretend.stub(
            status_code=200,
            json=pretend.call_recorder(lambda: {"boostrap": False}),
        )
        fake_response_post = pretend.stub(
            status_code=202,
            json=pretend.call_recorder(
                lambda: {
                    "detail": "Unexpected error, message queue connection"
                }
            ),
            text="<200> 'detail': 'Unexpected error, queue connection'",
        )
        mocked_request_server = MagicMock()
        mocked_request_server.side_effect = [
            fake_response_get,
            fake_response_post,
        ]

        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony.request_server",
            mocked_request_server,
        )

        class FakeKey:
            def __init__(self):
                self.error = None
                self.key = generate_ed25519_key()

        fake__load_key = pretend.call_recorder(lambda *a, **kw: FakeKey())
        monkeypatch.setattr(
            "kaprien.cli.admin.ceremony._load_key", fake__load_key
        )

        # simulate the settings file
        test_context["settings"].SERVER = "fake-server"
        test_context["settings"].TOKEN = "test-token"
        # write settings
        test_result = client.invoke(
            ceremony,
            ["--bootstrap"],
            input="\n".join(input_step1 + input_step2),
            obj=test_context,
        )

        assert test_result.exit_code == 1
        assert "Unexpected error, queue connection" in test_result.output